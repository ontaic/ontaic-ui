# Deployment Guide

This guide covers deploying your Ontaic application to various hosting platforms.

## Overview

Ontaic applications compile to static files (HTML, CSS, JavaScript, WASM) that can be deployed to any static hosting provider. No server is required for the frontend.

## Build for Production

```bash
# Build the WASM runtime
wasm-pack build --target web --release crates/ontaic-runtime

# Compile your Python components
python -c "from ontaic.compiler import OntaicCompiler; OntaicCompiler().compile_directory('.', 'dist/schema.json')"

# Copy files to dist directory
cp index.html dist/
cp -r src/ dist/src/
cp public/pkg/ dist/pkg/
```

## Vercel

### Automatic Deployment

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Configure:
   - **Framework Preset**: Other
   - **Build Command**: `wasm-pack build --target web --release crates/ontaic-runtime && python -c "from ontaic.compiler import OntaicCompiler; OntaicCompiler().compile_directory('.', 'dist/schema.json')"`
   - **Output Directory**: `dist`
5. Deploy

### vercel.json

```json
{
  "buildCommand": "wasm-pack build --target web --release crates/ontaic-runtime",
  "outputDirectory": "dist",
  "framework": null
}
```

### CLI Deployment

```bash
npm i -g vercel
vercel login
vercel --prod
```

## Netlify

### Automatic Deployment

1. Push your code to GitHub
2. Go to [netlify.com](https://netlify.com)
3. Import your repository
4. Configure:
   - **Build Command**: `wasm-pack build --target web --release crates/ontaic-runtime`
   - **Publish Directory**: `dist`
5. Deploy

### netlify.toml

```toml
[build]
  command = "wasm-pack build --target web --release crates/ontaic-runtime"
  publish = "dist"

[[headers]]
  for = "/*"
  [headers.values]
    Cross-Origin-Opener-Policy = "same-origin"
    Cross-Origin-Embedder-Policy = "require-corp"
```

### CLI Deployment

```bash
npm i -g netlify-cli
netlify login
netlify deploy --prod
```

## Cloudflare Pages

### Automatic Deployment

1. Push your code to GitHub
2. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
3. Connect your repository
4. Configure:
   - **Build Command**: `wasm-pack build --target web --release crates/ontaic-runtime`
   - **Build Output Directory**: `dist`
5. Deploy

### wrangler.toml

```toml
name = "ontaic-app"
type = "webpack"
account_id = ""
workers_dev = true

[site]
bucket = "./dist"
```

### CLI Deployment

```bash
npm i -g wrangler
wrangler login
wrangler pages deploy dist
```

## GitHub Pages

### Automatic Deployment

1. Go to your repository settings
2. Navigate to Pages
3. Select GitHub Actions as the source

### .github/workflows/deploy.yml

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          
      - name: Install wasm-pack
        run: curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
        
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          pip install -e python/
          
      - name: Build WASM
        run: wasm-pack build --target web --release crates/ontaic-runtime
        
      - name: Compile schema
        run: python -c "from ontaic.compiler import OntaicCompiler; OntaicCompiler().compile_directory('.', 'dist/schema.json')"
        
      - name: Prepare dist
        run: |
          cp index.html dist/
          cp -r src/ dist/src/
          cp -r public/pkg/ dist/pkg/
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## AWS S3 + CloudFront

### 1. Create S3 Bucket

```bash
aws s3 mb s3://my-ontaic-app
```

### 2. Enable Static Website Hosting

```bash
aws s3 website s3://my-ontaic-app \
  --index-document index.html \
  --error-document index.html
```

### 3. Upload Files

```bash
aws s3 sync dist/ s3://my-ontaic-app
```

### 4. Create CloudFront Distribution

```bash
aws cloudfront create-distribution \
  --origin-domain-name my-ontaic-app.s3.amazonaws.com \
  --default-root-object index.html
```

## Firebase Hosting

### 1. Initialize Firebase

```bash
firebase init hosting
```

### 2. Configure firebase.json

```json
{
  "hosting": {
    "public": "dist",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "**/*.wasm",
        "headers": [
          {
            "key": "Content-Type",
            "value": "application/wasm"
          }
        ]
      }
    ]
  }
}
```

### 3. Deploy

```bash
firebase deploy
```

## Docker

### Dockerfile

```dockerfile
FROM rust:latest as rust-builder

RUN curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

WORKDIR /app
COPY . .

RUN wasm-pack build --target web --release crates/ontaic-runtime

FROM python:3.10-slim as python-builder

WORKDIR /app
COPY --from=rust-builder /app .

RUN pip install -e python/

RUN python -c "from ontaic.compiler import OntaicCompiler; OntaicCompiler().compile_directory('.', 'dist/schema.json')"

FROM nginx:alpine

COPY --from=python-builder /app/dist /usr/share/nginx/html
COPY --from=python-builder /app/index.html /usr/share/nginx/html/
COPY --from=python-builder /app/src /usr/share/nginx/html/src
COPY --from=python-builder /app/public/pkg /usr/share/nginx/html/pkg

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Build and Run

```bash
docker build -t ontaic-app .
docker run -p 8080:80 ontaic-app
```

## Environment Variables

### Runtime Configuration

Create a `config.js` file:

```javascript
const config = {
  API_URL: process.env.API_URL || 'https://api.example.com',
  WS_URL: process.env.WS_URL || 'ws://localhost:8765',
  ENVIRONMENT: process.env.ENVIRONMENT || 'development',
};

window.ONTAIC_CONFIG = config;
```

### Build-time Variables

Use Vite's environment variables:

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_WS_URL=ws://localhost:8765
```

```javascript
// Access in your code
const apiUrl = import.meta.env.VITE_API_URL;
```

## Performance Optimization

### Enable WASM Streaming

```html
<script>
  if ('WebAssembly' in window) {
    WebAssembly.instantiateStreaming(fetch('/pkg/ontaic_runtime_bg.wasm'))
      .then(result => {
        window.wasmModule = result.instance.exports;
      });
  }
</script>
```

### Lazy Loading

```javascript
// Load schema on demand
async function loadSchema() {
  const response = await fetch('/schema.json');
  return await response.json();
}
```

### Compression

Enable gzip/brotli compression on your hosting platform:

```nginx
# nginx.conf
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript application/wasm;
gzip_min_length 256;
```

## Troubleshooting

### WASM Not Loading

Ensure correct MIME type:
```
.wasm -> application/wasm
```

### CORS Issues

Add headers:
```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

### 404 on Refresh

Configure SPA fallback to serve `index.html` for all routes.

## Next Steps

- Set up CI/CD pipeline
- Configure custom domain
- Set up monitoring and analytics
- Implement error tracking
