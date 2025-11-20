"""React templates for code generation."""

REACT_APP_TEMPLATE = '''import React, {{ useState, useEffect }} from 'react';
import './App.css';

function App() {{
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {{
    fetchData();
  }}, []);

  const fetchData = async () => {{
    try {{
      const response = await fetch(`${{API_URL}}/{resource_plural}`);
      const result = await response.json();
      setData(result.data || []);
      setLoading(false);
    }} catch (error) {{
      console.error('Error fetching data:', error);
      setLoading(false);
    }}
  }};

  const handleCreate = async (item) => {{
    try {{
      await fetch(`${{API_URL}}/{resource_plural}`, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(item)
      }});
      fetchData();
    }} catch (error) {{
      console.error('Error creating item:', error);
    }}
  }};

  const handleDelete = async (id) => {{
    try {{
      await fetch(`${{API_URL}}/{resource_plural}/${{id}}`, {{
        method: 'DELETE'
      }});
      fetchData();
    }} catch (error) {{
      console.error('Error deleting item:', error);
    }}
  }};

  if (loading) {{
    return <div className="App"><h2>Loading...</h2></div>;
  }}

  return (
    <div className="App">
      <header className="App-header">
        <h1>{project_name}</h1>
      </header>
      <main className="App-main">
        <div className="items-list">
          {{data.length === 0 ? (
            <p>No items yet. Add one below!</p>
          ) : (
            data.map((item, index) => (
              <div key={{index}} className="item-card">
                <pre>{{JSON.stringify(item, null, 2)}}</pre>
                <button onClick={{() => handleDelete(index)}}>Delete</button>
              </div>
            ))
          )}}
        </div>
      </main>
    </div>
  );
}}

export default App;
'''

REACT_CSS_TEMPLATE = '''.App {{
  text-align: center;
  min-height: 100vh;
  background-color: #282c34;
  color: white;
}}

.App-header {{
  background-color: #1a1d23;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.App-header h1 {{
  margin: 0;
  font-size: 2.5rem;
}}

.App-main {{
  padding: 40px 20px;
}}

.items-list {{
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}}

.item-card {{
  background: #1a1d23;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  transition: transform 0.2s;
}}

.item-card:hover {{
  transform: translateY(-5px);
}}

.item-card pre {{
  text-align: left;
  background: #0d0f12;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 15px;
}}

.item-card button {{
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}}

.item-card button:hover {{
  background-color: #c0392b;
}}
'''

REACT_PACKAGE_JSON = '''{{
  "name": "{project_name_lower}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }},
  "eslintConfig": {{
    "extends": [
      "react-app"
    ]
  }},
  "browserslist": {{
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }}
}}
'''

REACT_INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{project_name} - Full Stack Application" />
    <title>{project_name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''

REACT_INDEX_JS = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''

REACT_INDEX_CSS = '''* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}

code {{
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
}}
'''

REACT_DOCKERFILE = '''FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''
