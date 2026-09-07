import sys
from dotenv import load_dotenv
load_dotenv()

from agents.ceo_agent import CEOAgent
from memory.business_memory import BusinessMemory
from services.approval_manager import ApprovalManager

def print_help():
    print("""
==================================================
AUTOBIZ AI CEO
==================================================
Commands:
  python ceo.py autonomous [--manual]  - Run continuous hands-free autonomous business engine
  python ceo.py new                  - Start a new business/product cycle
  python ceo.py cycles               - View all historical and active cycles
  python ceo.py history              - View historical and active products
  python ceo.py run <objective>      - Set objective and run active cycle
  python ceo.py run                  - Run next cycle step
  python ceo.py status [--cycle ID]  - View active cycle or specific cycle state
  python ceo.py tasks [--cycle ID]   - View tasks for cycle
  python ceo.py approvals            - View pending approvals for active cycle
  python ceo.py approve <id>         - Approve an action
  python ceo.py reject <id>          - Reject an action
  python ceo.py demo                 - Run local demo simulation (DEMO DATA ONLY)
  python ceo.py report               - Generate full report
    """)

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1].lower()
    agent = CEOAgent()
    memory = BusinessMemory()
    app_manager = ApprovalManager()

    if cmd == "new":
        new_state = memory.create_new_cycle()
        print("""
==================================================
NEW BUSINESS CYCLE INITIALIZED
==================================================
Active Cycle ID: {}
Current Product: None
Current Stage: NO_PRODUCT

Historical tasks, approvals, products, and analytics preserved.
Ready to run new objective with: python ceo.py run "<objective>"
        """.format(new_state.cycle_id))

    elif cmd == "cycles":
        cycles = memory.get_all_cycles()
        print("""
==================================================
BUSINESS CYCLES HISTORY
==================================================
        """)
        for c in cycles:
            print(f"CYCLE {c['cycle_id']}")
            print(f"Product: {c['product'] or 'None'}")
            print(f"Stage: {c['stage']}")
            print(f"Status: {c['status']}")
            print(f"Created: {c['created_at'][:10] if c.get('created_at') else 'N/A'}\n")

    elif cmd == "history":
        cycles = memory.get_all_cycles()
        print("""
==================================================
HISTORICAL & ACTIVE PRODUCTS
==================================================
        """)
        for c in cycles:
            print(f"Cycle {c['cycle_id']}: {c['product'] or 'None'}")
            print(f"  Stage: {c['stage']}")
            print(f"  Status: {c['status']}\n")

    elif cmd == "run":
        if len(sys.argv) > 2:
            objective = " ".join(sys.argv[2:])
            print(f"Objective received: {objective}")
            state = memory.get_business_state()
            if state.product is None or state.stage == "NO_PRODUCT":
                state.stage = "NO_PRODUCT"
                state.research_results = None
                memory.update_business_state(state)
            agent.set_objective(objective)
        agent.run_cycle()

    elif cmd == "status":
        target_cycle = None
        if "--cycle" in sys.argv:
            idx = sys.argv.index("--cycle")
            if idx + 1 < len(sys.argv):
                target_cycle = int(sys.argv[idx + 1])
                
        state = memory.get_business_state(cycle_id=target_cycle)
        c_id = target_cycle or state.cycle_id
        cycle_approvals = memory.get_approvals_for_cycle(cycle_id=c_id)
        deploy_app = next((a for a in cycle_approvals if a.action == "DEPLOY_PRODUCT"), None)

        print(f"Cycle ID: {state.cycle_id}")
        print(f"Product: {state.product or 'None'}")
        print(f"Stage: {state.stage}")
        print(f"QA: {state.qa or 'None'}")

        if deploy_app:
            est_cost = deploy_app.estimated_cost
            est_str = f"${est_cost:.0f}" if est_cost.is_integer() else f"${est_cost:.2f}"
            act_cost = deploy_app.actual_cost if deploy_app.deployment_mode != "LOCAL/DEMO" else 0.0
            act_str = f"${act_cost:.0f}" if act_cost.is_integer() else f"${act_cost:.2f}"
            print(f"Estimated deployment cost: {est_str}")
            print(f"Actual expenditure: {act_str}")
            print(f"Deployment: {deploy_app.deployment_mode}")
        else:
            print(f"Deployment: {state.deployment or 'None'}")

        print(f"Marketing: {state.marketing or 'None'}")
        
    elif cmd == "tasks":
        target_cycle = None
        if "--cycle" in sys.argv:
            idx = sys.argv.index("--cycle")
            if idx + 1 < len(sys.argv):
                target_cycle = int(sys.argv[idx + 1])
                
        tasks = memory.get_all_tasks(cycle_id=target_cycle)
        print(f"TASKS (Cycle {target_cycle or memory.get_active_cycle_id()}):")
        for t in tasks:
            print(f"[{t.task_id}] (Cycle {t.cycle_id}) {t.type} - {t.status}")

    elif cmd == "approvals":
        c_id = memory.get_active_cycle_id()
        if "--cycle" in sys.argv:
            idx = sys.argv.index("--cycle")
            if idx + 1 < len(sys.argv):
                c_id = int(sys.argv[idx + 1])
        apps = memory.get_pending_approvals(cycle_id=c_id)
        print(f"PENDING APPROVALS (Cycle {c_id}):")
        if not apps:
            print("None.")
        for a in apps:
            est_cost = f"${a.estimated_cost:.0f}" if a.estimated_cost.is_integer() else f"${a.estimated_cost:.2f}"
            act_cost = a.actual_cost if a.deployment_mode != "LOCAL/DEMO" else 0.0
            act_str = f"${act_cost:.0f}" if act_cost.is_integer() else f"${act_cost:.2f}"
            mode_label = f", Mode: {a.deployment_mode}" if a.deployment_mode else ""
            print(f"[{a.approval_id}] (Cycle {a.cycle_id}) {a.action}: {a.description} (Risk: {a.risk_level}, Est. Cost: {est_cost}, Actual Exp: {act_str}{mode_label})")

    elif cmd == "approve":
        if len(sys.argv) < 3:
            print("Usage: python ceo.py approve <id>")
            return
        app_id = int(sys.argv[2])
        app_manager.approve(app_id)
        from models.msa_db import get_db
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE posts SET status='APPROVED' WHERE post_id=?", (app_id,))
        conn.commit()
        conn.close()
        print(f"Approval {app_id} APPROVED.")
        
    elif cmd == "reject":
        if len(sys.argv) < 3:
            print("Usage: python ceo.py reject <id>")
            return
        app_id = int(sys.argv[2])
        app_manager.reject(app_id)
        from models.msa_db import get_db
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE posts SET status='CANCELLED' WHERE post_id=?", (app_id,))
        conn.commit()
        conn.close()
        print(f"Approval {app_id} REJECTED.")

    elif cmd == "demo":
        print("""
==================================================
DEMO SIMULATION MODE — DEMO DATA ONLY (NO REAL REVENUE)
==================================================
- Money spent: $0.00 (No financial transactions executed)
- Real emails: 0 sent
- Public deployment: Local simulation only
- Marketing: Local demo copy generated
        """)
        agent.run_cycle()
        
    elif cmd == "report":
        target_cycle = None
        if "--cycle" in sys.argv:
            idx = sys.argv.index("--cycle")
            if idx + 1 < len(sys.argv):
                target_cycle = int(sys.argv[idx + 1])

        state = memory.get_business_state(cycle_id=target_cycle)
        c_id = target_cycle or state.cycle_id
        cycle_approvals = memory.get_approvals_for_cycle(cycle_id=c_id)
        deploy_app = next((a for a in cycle_approvals if a.action == "DEPLOY_PRODUCT"), None)

        print("CEO ORCHESTRATOR REPORT")
        print("=======================")
        print(f"Cycle ID: {state.cycle_id}")
        print(f"Current Product: {state.product or 'None'}")
        print(f"Current Stage: {state.stage}")
        print(f"Research: {'PASS' if state.research_results else 'PENDING'}")
        print(f"Build: {'PASS' if state.build_status else 'PENDING'}")
        print(f"QA: {'PASS' if state.qa == 'PASS' else state.qa if state.qa else 'PENDING'}")

        if deploy_app:
            est_cost = deploy_app.estimated_cost
            est_str = f"${est_cost:.0f}" if est_cost.is_integer() else f"${est_cost:.2f}"
            act_cost = deploy_app.actual_cost if deploy_app.deployment_mode != "LOCAL/DEMO" else 0.0
            act_str = f"${act_cost:.0f}" if act_cost.is_integer() else f"${act_cost:.2f}"
            print(f"Estimated deployment cost: {est_str}")
            print(f"Actual expenditure: {act_str}")
            print(f"Deployment: {deploy_app.deployment_mode}")
        else:
            dep_status = state.deployment if state.deployment else 'PENDING'
            print(f"Deployment: {dep_status}")

        print(f"Marketing: {state.marketing if state.marketing else 'PENDING'}")
        print(f"Customers: {state.customers} (DEMO DATA — NOT REAL)")
        print(f"Revenue: ${state.revenue:.2f} (DEMO DATA — NOT REAL)")

        print("\nApprovals Summary:")
        if not cycle_approvals:
            print("None.")
        for a in cycle_approvals:
            est_cost = f"${a.estimated_cost:.0f}" if a.estimated_cost.is_integer() else f"${a.estimated_cost:.2f}"
            act_cost = a.actual_cost if a.deployment_mode != "LOCAL/DEMO" else 0.0
            act_str = f"${act_cost:.0f}" if act_cost.is_integer() else f"${act_cost:.2f}"
            print(f"- [{a.approval_id}] (Cycle {a.cycle_id}) {a.action} (Est. Cost: {est_cost}, Actual Exp: {act_str}, Mode: {a.deployment_mode}, Status: {a.status})")
            
    elif cmd == "social":
        subcmd = sys.argv[2].lower() if len(sys.argv) > 2 else "status"
        from services.instagram_service import InstagramService
        from marketing.connectors.facebook import FacebookConnector
        from marketing.connectors.instagram import InstagramConnector
        from marketing.connectors.linkedin import LinkedInConnector
        from marketing.connectors.x import XConnector
        from marketing.connectors.reddit import RedditConnector
        from models.msa_db import get_db

        ig_service = InstagramService()
        connectors = {
            "instagram": InstagramConnector(),
            "facebook": FacebookConnector(),
            "linkedin": LinkedInConnector(),
            "x": XConnector(),
            "reddit": RedditConnector()
        }

        state = memory.get_business_state()
        c_id = state.cycle_id

        if subcmd in ("status", ""):
            print("SOCIAL ACCOUNTS")
            for plat_name in ["Instagram", "Facebook", "LinkedIn", "X", "Reddit"]:
                conn_obj = connectors[plat_name.lower()]
                val = conn_obj.validate_connection()
                st = "CONNECTED" if val.get("oauth_connected") else "NOT CONNECTED"
                if plat_name == "Instagram" and st == "CONNECTED":
                    print(f"Instagram: {st}")
                    print(f"Instagram Account: {val.get('account_name', 'autobizai01')}")
                    print(f"Instagram ID: {val.get('account_id', '17841437441178441')}")
                else:
                    print(f"{plat_name}: {st}")
            print()

        elif subcmd == "test":
            res = ig_service.test_connection()
            status_text = res.get("status", "FAIL")
            print("==================================================")
            print(f"INSTAGRAM CONNECTION TEST: {status_text}")
            print("==================================================")
            print(f"Instagram connection: {status_text}")
            if status_text == "PASS":
                print(f"Account Username: @{res.get('account_name', 'autobizai01')}")
                print(f"Account ID: {res.get('account_id', '17841437441178441')}")
                print(f"Account Type: {res.get('account_type', 'BUSINESS')}")
            else:
                print(f"Reason: {res.get('reason', 'Failed to authenticate')}")
            print()

        elif subcmd in ("create-post", "create_post"):
            from agents.marketing_sales_analytics_agent import MarketingSalesAnalyticsAgent
            msa = MarketingSalesAnalyticsAgent()
            msa_res = msa.run("Create marketing for current product")

            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM posts WHERE cycle_id=? AND platform='instagram' ORDER BY post_id DESC LIMIT 1", (c_id,))
            post = c.fetchone()

            headline = post['headline'] if post else "Automated Clinic Billing Workflow Prototype"
            caption_text = post['caption'] if post else "Streamlines invoice tracking and claim matching for small medical practices."
            hashtags = post['hashtags'] if post else "#ClinicAutomation #MedicalBilling #WorkflowPrototype"
            image_url = (post['media_prompt'] if post and post['media_prompt'] else "https://autobiz.local/assets/medical_billing_preview.png")

            full_caption = f"{headline}\n\n{caption_text}\n\n{hashtags}".strip()

            app_id = app_manager.request_approval(
                action="PUBLISH_INSTAGRAM_POST",
                description=f"Approve publishing Instagram post for '{state.product or 'Cycle 5 Product'}': '{headline}'",
                risk_level="HIGH",
                estimated_cost=0.0,
                actual_cost=0.0,
                demo_cost=0.0,
                deployment_mode="LOCAL/DEMO",
                cycle_id=c_id
            )

            print("==================================================")
            print("POST PREVIEW")
            print("==================================================")
            print("Platform: Instagram")
            print(f"Caption:\n{full_caption}")
            print(f"Image: {image_url}")
            print(f"Approval ID: {app_id}")
            print("Status: WAITING_APPROVAL")
            print("==================================================")

        elif subcmd == "approvals":
            pending = app_manager.get_pending_approvals(cycle_id=c_id)
            social_pending = [a for a in pending if "INSTAGRAM" in a.action or "MARKETING" in a.action or "SOCIAL" in a.action]
            print("==================================================")
            print(f"PENDING SOCIAL APPROVALS (Cycle {c_id})")
            print("==================================================")
            if not social_pending:
                print("No pending social approvals found.")
            for a in social_pending:
                print(f"- [{a.approval_id}] Action: {a.action} | Status: {a.status}")
                print(f"  Description: {a.description}\n")

        elif subcmd == "approve":
            if len(sys.argv) < 4:
                print("Error: Missing approval ID. Usage: python ceo.py social approve <approval_id>")
            else:
                try:
                    app_id = int(sys.argv[3])
                    success = app_manager.approve(app_id)
                    if success:
                        print(f"SUCCESS: Social approval [{app_id}] APPROVED.")
                        print(f"Run 'python ceo.py social publish {app_id}' to execute publishing.")
                    else:
                        print(f"ERROR: Approval [{app_id}] not found or already processed.")
                except ValueError:
                    print("Error: Approval ID must be an integer.")

        elif subcmd == "publish":
            if len(sys.argv) < 4:
                print("Error: Missing approval ID. Usage: python ceo.py social publish <approval_id>")
            else:
                try:
                    app_id = int(sys.argv[3])
                    approval = app_manager.memory.get_approval(app_id)

                    if not approval:
                        print(f"ERROR: Approval ID [{app_id}] does not exist.")
                        return

                    if approval.cycle_id != c_id:
                        print(f"ERROR: Approval [{app_id}] belongs to Cycle {approval.cycle_id}, but active cycle is {c_id}.")
                        return

                    if approval.status != "APPROVED":
                        print(f"ERROR: Approval [{app_id}] status is '{approval.status}'. Must be 'APPROVED'. Run 'python ceo.py social approve {app_id}' first.")
                        return

                    if "INSTAGRAM" not in approval.action and "MARKETING" not in approval.action:
                        print(f"ERROR: Approval [{app_id}] action is '{approval.action}', not an Instagram post approval.")
                        return

                    conn = get_db()
                    c = conn.cursor()
                    c.execute("SELECT * FROM posts WHERE cycle_id=? AND platform='instagram' ORDER BY post_id DESC LIMIT 1", (c_id,))
                    post = c.fetchone()
                    post_dict = dict(post) if post else {}

                    headline = post_dict.get("headline", "Clinic Billing Workflow Prototype")
                    caption_body = post_dict.get("caption", "Automated invoice tracking for independent practices.")
                    hashtags = post_dict.get("hashtags", "#MedicalBilling #ClinicAutomation")
                    full_caption = f"{headline}\n\n{caption_body}\n\n{hashtags}".strip()
                    image_url = post_dict.get("image_url") or "https://autobiz.local/assets/medical_billing_preview.png"

                    if not ig_service.access_token or ig_service.access_token.startswith("your_"):
                        err_msg = "Missing or placeholder INSTAGRAM_ACCESS_TOKEN in environment (.env)"
                        print(f"ERROR: {err_msg}. Publishing aborted.")
                        c.execute("""
                            INSERT INTO posts (cycle_id, platform, content_type, caption, headline, cta, hashtags, media_prompt, status, error_message)
                            VALUES (?, 'instagram', 'PUBLISH', ?, ?, '', ?, ?, 'FAILED', ?)
                        """, (c_id, full_caption, headline, hashtags, image_url, err_msg))
                        conn.commit()
                        conn.close()
                        return

                    print(f"Executing 2-Step Instagram Publishing Flow for Approval [{app_id}]...")
                    print("Step 1: Creating Media Container...")
                    c_res = ig_service.create_media(image_url, full_caption)

                    if c_res.get("status") != "SUCCESS":
                        err_msg = c_res.get("error", "Container creation failed")
                        print(f"FAILED Step 1: {err_msg}")
                        c.execute("""
                            INSERT INTO posts (cycle_id, platform, content_type, caption, headline, cta, hashtags, media_prompt, status, error_message)
                            VALUES (?, 'instagram', 'PUBLISH', ?, ?, '', ?, ?, 'FAILED', ?)
                        """, (c_id, full_caption, headline, hashtags, image_url, err_msg))
                        conn.commit()
                        conn.close()
                        return

                    container_id = c_res["container_id"]
                    print(f"Step 1 PASS: Media Container created (ID: {container_id})")
                    print("Step 2: Publishing Media Container...")
                    p_res = ig_service.publish_media(container_id)

                    if p_res.get("status") == "SUCCESS":
                        pub_id = p_res["published_post_id"]
                        pub_url = p_res["url"]
                        print("==================================================")
                        print(f"SUCCESS: Published to Instagram! Post ID: {pub_id}")
                        print(f"URL: {pub_url}")
                        print("==================================================")

                        c.execute("""
                            INSERT INTO posts (cycle_id, platform, content_type, caption, headline, cta, hashtags, media_prompt, status, platform_post_id, published_at, url, post_url)
                            VALUES (?, 'instagram', 'PUBLISHED', ?, ?, '', ?, ?, 'PUBLISHED', ?, ?, ?, ?)
                        """, (c_id, full_caption, headline, hashtags, image_url, pub_id, p_res["published_at"], pub_url, pub_url))
                        conn.commit()
                    else:
                        err_msg = p_res.get("error", "Media publish failed")
                        print(f"FAILED Step 2: {err_msg}")
                        c.execute("""
                            INSERT INTO posts (cycle_id, platform, content_type, caption, headline, cta, hashtags, media_prompt, status, error_message)
                            VALUES (?, 'instagram', 'PUBLISH', ?, ?, '', ?, ?, 'FAILED', ?)
                        """, (c_id, full_caption, headline, hashtags, image_url, err_msg))
                        conn.commit()

                    conn.close()

                except ValueError:
                    print("Error: Approval ID must be an integer.")

        elif subcmd in connectors:
            conn_obj = connectors[subcmd]
            res = conn_obj.connect()
            print("==================================================")
            print(f"STARTING {subcmd.upper()} OAUTH CONNECTION FLOW")
            print("==================================================")
            print(f"Status: {res.get('status')}")
            if res.get("oauth_url"):
                print(f"OAuth URL: {res.get('oauth_url')}")
            print(f"Message: {res.get('message', res.get('reason', 'Authorization required.'))}")
        else:
            print("Usage: python ceo.py social [status|test|create-post|approvals|approve <id>|publish <id>]")

    elif cmd == "marketing":
        subargs = [a.lower() for a in sys.argv[2:]]
        is_dry_run = "--dry-run" in subargs or "dry-run" in subargs
        subcmd = next((a for a in subargs if not a.startswith("--")), "run")

        from models.msa_db import get_db
        from agents.marketing_sales_analytics_agent import MarketingSalesAnalyticsAgent
        from marketing.connectors.facebook import FacebookConnector
        from marketing.connectors.instagram import InstagramConnector
        from marketing.connectors.linkedin import LinkedInConnector
        from marketing.connectors.x import XConnector
        from marketing.connectors.reddit import RedditConnector
        from marketing.analytics import AnalyticsManager

        connectors = {
            "instagram": InstagramConnector(),
            "facebook": FacebookConnector(),
            "linkedin": LinkedInConnector(),
            "x": XConnector(),
            "reddit": RedditConnector()
        }

        conn = get_db()
        c = conn.cursor()
        state = memory.get_business_state()
        c_id = state.cycle_id

        if is_dry_run or subcmd == "dry-run":
            import os
            os.environ["SOCIAL_DRY_RUN"] = "true"
            msa_agent = MarketingSalesAnalyticsAgent()
            res = msa_agent.run("Create marketing for current product")
            print("""
==================================================
MARKETING CAMPAIGN SIMULATION (DRY RUN MODE)
==================================================
            """)
            c.execute("SELECT * FROM posts WHERE cycle_id=? ORDER BY post_id ASC", (c_id,))
            posts = c.fetchall()
            for p in posts:
                plat = p['platform'].lower()
                conn_obj = connectors.get(plat)
                conn_status = conn_obj.validate_connection() if conn_obj else {"status": "NOT_CONNECTED"}
                pub_res = conn_obj.publish_post(dict(p)) if conn_obj else {"status": "NOT_CONNECTED"}
                print(f"PLATFORM: {p['platform'].capitalize()}")
                print(f"POST: Headline: {p['headline']} | Caption: {p['caption']}")
                print(f"ACCOUNT CONNECTION: {conn_status.get('status', 'NOT_CONNECTED')}")
                print(f"STATUS: READY — NOT PUBLISHED (Dry Run Result: {pub_res.get('status')})\n")

        elif subcmd in ("run", "generate", "dashboard"):
            msa_agent = MarketingSalesAnalyticsAgent()
            res = msa_agent.run("Create marketing for current product")
            print(res.get("result", "Marketing campaign generated."))

        elif subcmd == "posts":
            print(f"""
==================================================
CAMPAIGN POSTS (Cycle {c_id})
==================================================
""")
            c.execute("SELECT * FROM posts WHERE cycle_id=? ORDER BY post_id ASC", (c_id,))
            all_posts = c.fetchall()
            if not all_posts:
                print("No campaign posts found. Run 'python ceo.py marketing' to generate campaign.")
            for p in all_posts:
                print(f"[{p['post_id']}] Platform: {p['platform'].capitalize()} | Type: {p['content_type']}")
                print(f"  Headline: {p['headline']}")
                print(f"  Caption: {p['caption']}")
                print(f"  CTA: {p['cta']}")
                print(f"  Hashtags: {p['hashtags']}")
                print(f"  Status: {p['status']}\n")

        elif subcmd == "analytics":
            print(f"""
==================================================
MARKETING ANALYTICS REPORT (Cycle {c_id})
==================================================
""")
            mgr = AnalyticsManager(connectors)
            c.execute("SELECT * FROM posts WHERE cycle_id=? ORDER BY post_id ASC", (c_id,))
            all_posts = c.fetchall()
            if not all_posts:
                print("No posts found to analyze. Run 'python ceo.py marketing' first.")
            for p in all_posts:
                post_id = p.get('platform_post_id') or p.get('post_id')
                metrics_res = mgr.get_post_analytics(p['platform'], str(post_id))
                source_tag = metrics_res['source']
                print(f"[{p['post_id']}] Platform: {p['platform'].capitalize()} | Headline: {p['headline']}")
                print(f"  SOURCE: [{source_tag}]")
                print(f"  Metrics: {metrics_res.get('metrics', {})}\n")

        elif subcmd == "live":
            target_plat = sys.argv[3].lower() if len(sys.argv) > 3 else "facebook"
            if target_plat not in connectors:
                print(f"Invalid platform '{target_plat}'. Supported platforms: instagram, facebook, linkedin, x, reddit.")
                return

            conn_obj = connectors[target_plat]
            val = conn_obj.validate_connection()
            if val["status"] != "CONNECTED":
                print(f"ERROR:\nSocial account NOT CONNECTED for {target_plat.capitalize()}: {val.get('reason')}")
                print(f"Run 'python ceo.py social {target_plat}' to initiate OAuth connection.")
                return

            c.execute("SELECT * FROM posts WHERE cycle_id=? AND platform=? AND status='APPROVED' LIMIT 1", (c_id, target_plat))
            approved_post = c.fetchone()
            if not approved_post:
                print(f"No APPROVED {target_plat.capitalize()} posts found. Run 'python ceo.py approve <id>' first.")
            else:
                print(f"Publishing post [{approved_post['post_id']}] to {target_plat.capitalize()} via Official API...")
                pub_res = conn_obj.publish_post(dict(approved_post))
                if pub_res["status"] in ("PUBLISHED", "DRY_RUN"):
                    c.execute("UPDATE posts SET status='PUBLISHED', platform_post_id=?, published_at=?, url=?, post_url=? WHERE post_id=?",
                              (pub_res['platform_post_id'], pub_res['published_at'], pub_res['url'], pub_res['url'], approved_post['post_id']))
                    conn.commit()
                    print(f"SUCCESS: Published to {target_plat.capitalize()}! Post ID: {pub_res['platform_post_id']}")
                    print(f"URL: {pub_res['url']}")
                else:
                    c.execute("UPDATE posts SET error_message=? WHERE post_id=?", (pub_res.get('error'), approved_post['post_id']))
                    conn.commit()
                    print(f"FAILED to publish: {pub_res.get('error')}")

        conn.close()

    elif cmd in ["autonomous", "auto"]:
        from auto_runner import AutonomousRunner
        auto_approve = "--manual" not in sys.argv
        max_cycles = 5
        for arg in sys.argv:
            if arg.startswith("--cycles="):
                max_cycles = int(arg.split("=")[1])
        runner = AutonomousRunner(auto_approve=auto_approve, max_cycles=max_cycles)
        runner.run()

    else:
        print_help()

if __name__ == "__main__":
    main()
