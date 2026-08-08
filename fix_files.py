import os

b_dir = r'workspace\generated_projects\student-expense-tracker\backend'
f_dir = r'workspace\generated_projects\student-expense-tracker\frontend'
src_dir = os.path.join(f_dir, 'src')

os.makedirs(b_dir, exist_ok=True)
os.makedirs(f_dir, exist_ok=True)
os.makedirs(src_dir, exist_ok=True)

with open(os.path.join(b_dir, 'requirements.txt'), 'w', encoding='utf-8') as f:
    f.write('fastapi\nuvicorn\npytest\n')

with open(os.path.join(f_dir, 'package.json'), 'w', encoding='utf-8') as f:
    f.write('''{
  "name": "student-expense-tracker",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0"
  }
}''')

with open(os.path.join(f_dir, 'vite.config.js'), 'w', encoding='utf-8') as f:
    f.write('''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})''')

with open(os.path.join(f_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Student Expense Tracker</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>''')

with open(os.path.join(src_dir, 'main.jsx'), 'w', encoding='utf-8') as f:
    f.write('''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)''')

with open(os.path.join(src_dir, 'App.jsx'), 'w', encoding='utf-8') as f:
    f.write('''import React from 'react'
function App() {
  return <div>Student Expense Tracker</div>
}
export default App''')
