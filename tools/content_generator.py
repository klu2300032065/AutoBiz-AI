import requests
import json
from tools.research_tools import query_ollama

def generate_marketing_strategy(product_name: str, product_desc: str) -> str:
    prompt = f"""
    Product: {product_name}
    Description: {product_desc}
    
    Act as an expert Chief Marketing Officer. Generate a marketing strategy.
    Include:
    1. Product positioning
    2. Value proposition
    3. Target audience segments
    """
    return query_ollama(prompt)

def generate_landing_page_copy(product_name: str, product_desc: str) -> str:
    prompt = f"""
    Write high-converting landing page copy for {product_name}.
    Description: {product_desc}
    
    Structure MUST follow:
    Problem -> Solution -> Benefit -> Evidence -> Call to Action
    """
    return query_ollama(prompt)

def generate_social_posts(product_name: str, product_desc: str) -> str:
    prompt = f"""
    Write 5 engaging social media posts for {product_name}.
    Description: {product_desc}
    Structure each post: Problem -> Solution -> Benefit -> Evidence -> Call to Action
    """
    return query_ollama(prompt)

def generate_email_drafts(product_name: str, product_desc: str) -> str:
    prompt = f"""
    Write 3 email marketing drafts (Welcome, Nurture, Sales) for {product_name}.
    Description: {product_desc}
    Structure each email: Problem -> Solution -> Benefit -> Evidence -> Call to Action
    """
    return query_ollama(prompt)

def generate_seo_metadata(product_name: str, product_desc: str) -> str:
    prompt = f"""
    Generate SEO metadata for {product_name}.
    Description: {product_desc}
    
    Provide:
    1. SEO Title (max 60 chars)
    2. Meta Description (max 160 chars)
    3. 10 Keywords
    """
    return query_ollama(prompt)
