# Deploying CloudMind AI Landing Page to GitHub Pages

This guide explains how to deploy the CloudMind AI landing page using GitHub Pages.

## Quick Setup

### 1. Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/NickScherbakov/cloudmind-ai`
2. Click **Settings** → **Pages** (in the left sidebar)
3. Under **Source**, select:
   - Branch: `main` (or your default branch)
   - Folder: `/ (root)`
4. Click **Save**

### 2. Wait for Deployment

GitHub will automatically build and deploy your site. This usually takes 1-3 minutes.

You can monitor the deployment:
- Go to **Actions** tab
- Look for the "pages build and deployment" workflow

### 3. Access Your Site

Once deployed, your site will be available at:
```
https://nickscherbakov.github.io/cloudmind-ai/
```

## Files Structure

The landing page consists of:

```
cloudmind-ai/
├── index.html          # Main landing page
├── styles.css          # Styles and responsive design
├── _config.yml         # Jekyll configuration for GitHub Pages
├── README.md           # Project documentation
├── CONTRIBUTOR_VISION.md
├── CONTRIBUTOR_VISION_RU.md
└── docs/               # Additional documentation
```

## Customization

### Update Site URL

If your GitHub username or repository name is different, update `_config.yml`:

```yaml
url: "https://YOUR_USERNAME.github.io"
baseurl: "/YOUR_REPO_NAME"
```

### Add Google Analytics (Optional)

1. Create a Google Analytics property
2. Add your tracking ID to `_config.yml`:

```yaml
google_analytics: UA-XXXXXXXX-X
```

### Modify Content

- **Hero section**: Edit the title and subtitle in `index.html`
- **Features**: Update feature cards with your specific capabilities
- **Roadmap**: Adjust timeline phases based on your actual roadmap
- **Styling**: Modify colors and gradients in `styles.css` (see `:root` variables)

## Custom Domain (Optional)

To use a custom domain (e.g., `cloudmind.ai`):

1. Add a `CNAME` file to the repository root:
   ```
   cloudmind.ai
   ```

2. Configure DNS records with your domain provider:
   - Add an A record pointing to GitHub Pages IPs:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - Or add a CNAME record pointing to: `nickscherbakov.github.io`

3. In GitHub Settings → Pages, enter your custom domain and save

## Local Development

To preview the landing page locally:

```bash
# Simple HTTP server (Python 3)
python -m http.server 8080

# Or using Node.js
npx http-server -p 8080

# Then open http://localhost:8080
```

For full Jekyll development:

```bash
# Install Jekyll
gem install bundler jekyll

# Create Gemfile (if needed)
bundle init
bundle add jekyll

# Serve locally
bundle exec jekyll serve

# Open http://localhost:4000
```

## Troubleshooting

### Page Not Loading
- Check GitHub Actions for build errors
- Ensure GitHub Pages is enabled in Settings
- Verify the branch and folder are correct

### Broken Links
- Relative links should work automatically
- For absolute links, use `{{ site.baseurl }}` in Jekyll templates
- Markdown files are automatically rendered by GitHub Pages

### Styling Issues
- Clear browser cache (Ctrl+F5 / Cmd+Shift+R)
- Check browser console for CSS loading errors
- Verify `styles.css` path in `index.html`

### 404 Errors
- If using a custom domain, ensure DNS is properly configured
- Check that file names match exactly (case-sensitive on Linux)

## Analytics & SEO

The landing page includes:
- ✅ Semantic HTML5 structure
- ✅ Meta tags for social sharing (Open Graph)
- ✅ Responsive design (mobile-first)
- ✅ Fast loading (minimal dependencies)
- ✅ Accessible navigation

To verify SEO:
1. Use Google Search Console
2. Submit sitemap: `https://nickscherbakov.github.io/cloudmind-ai/sitemap.xml`
3. Monitor indexing and performance

## Updates

To update the landing page:

```bash
# 1. Edit files locally
code index.html
code styles.css

# 2. Commit and push
git add index.html styles.css
git commit -m "Update landing page content"
git push origin main

# 3. GitHub Pages will automatically rebuild (1-3 minutes)
```

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [HTML5 Best Practices](https://developer.mozilla.org/en-US/docs/Learn/HTML)
- [Responsive Design Guide](https://web.dev/responsive-web-design-basics/)

---

**Questions?** Open an issue or check GitHub Pages deployment logs in the Actions tab.
