# Ontaic Website

This is the landing page and documentation website for Ontaic.

## Development

### Prerequisites
- Node.js 18+ (for Vite dev server)
- Python 3.10+ (for SDK)

### Local Development

1. Start the Vite dev server:
```bash
npm run dev
```

2. Open http://localhost:5173

### Build for Production

```bash
npm run build
```

Output will be in `dist/`.

## Structure

```
website/
├── index.html          # Landing page
├── docs/
│   └── index.html      # Documentation
├── examples/
│   └── index.html      # Examples
└── src/
    ├── style.css       # Global styles
    ├── main.js         # JavaScript
    ├── docs.css        # Docs page styles
    └── examples.css    # Examples page styles
```

## Deployment

The website can be deployed to:
- GitHub Pages
- Vercel
- Netlify
- Cloudflare Pages

Simply push to the `main` branch and the website will be deployed automatically if using GitHub Pages.
