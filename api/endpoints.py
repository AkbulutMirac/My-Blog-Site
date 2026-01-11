import os
from pathlib import Path
import fastapi
from fastapi import APIRouter, Cookie
import markdown
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from fastapi import Request
import time
import datetime
import re
# Get the Blog directory (parent of api folder)
BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter()
p = BASE_DIR / 'entries'
CORRECT_PASSWORD = 'HRV_-SV;1[HAtq]wgp{^E'


@router.get("/list_blog_posts")
def list_blog_posts():
    blog_posts = []
    for file in os.listdir(p):
        if file.endswith('.md'):
            slug = file[:-3]  # Remove the .md extension
            file_path = p / file
            try:
                # prefer creation time; fall back to modification time
                ts = file_path.stat().st_ctime
            except Exception:
                ts = file_path.stat().st_mtime
            dt = datetime.datetime.fromtimestamp(ts)
            date_str = dt.strftime('%Y-%m-%d %H:%M')
            blog_name = slug.replace('-', ' ').title()
            # try to read first heading from the markdown file to use as title
            title = ''
            try:
                with open(file_path, 'r', encoding='utf-8') as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        # look for markdown H1/H2 like '# Title' or '## Title'
                        if line.startswith('#'):
                            # remove leading # characters and surrounding whitespace
                            title = line.lstrip('#').strip()
                        break
            except Exception:
                title = ''
            # return lines like: slug|YYYY-MM-DD HH:MM|Title
            blog_posts.append(f"{slug}|{date_str}|{title}")
    blog_posts.sort(key=lambda x: x.split('|')[1], reverse=True)  # Sort by date descending
    return fastapi.Response(content="\n".join(blog_posts), media_type="text/plain")

@router.get("/blog/{slug}")
def blog(slug: str):
    """Markdown dosyasını okuyup HTML'e çevirir"""
    file_path = p / f"{slug}.md"
    if not file_path.exists():
        return fastapi.Response(status_code=404, content="Blog post not found")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'toc', 'codehilite']
    )
    
    
    full_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slug} - Mirac's Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --bg-color: #f5f0e8; --text-color: #1a1a1a; --text-muted: #666; --link-color: #5a4fcf; --link-hover: #4338ca; --border-color: #e0d8cc; }}
        body {{ font-family: 'Georgia', 'Times New Roman', serif; background-color: var(--bg-color); color: var(--text-color); line-height: 1.7; min-height: 100vh; display: flex; flex-direction: column; }}
        .container {{ max-width: 700px; margin: 0 auto; padding: 0 20px; width: 100%; }}
        header {{ padding: 30px 0; }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 700; font-size: 1.2rem; color: var(--text-color); text-decoration: none; }}
        nav {{ display: flex; align-items: center; gap: 25px; }}
        nav a {{ color: var(--text-muted); text-decoration: none; font-size: 0.95rem; transition: color 0.2s; }}
        nav a:hover {{ color: var(--text-color); }}
        .nav-icons {{ display: flex; gap: 15px; margin-left: 15px; padding-left: 15px; border-left: 1px solid var(--border-color); }}
        .nav-icons a, .nav-icons button {{ color: var(--text-muted); background: none; border: none; cursor: pointer; padding: 5px; display: flex; align-items: center; transition: color 0.2s; }}
        .nav-icons a:hover, .nav-icons button:hover {{ color: var(--text-color); }}
        .nav-icons svg {{ width: 18px; height: 18px; }}
        main {{ flex: 1; padding: 40px 0; }}
        .divider {{ height: 1px; background: var(--border-color); margin-bottom: 50px; }}
        .post-content {{ background: var(--bg-color); border-radius: 12px; box-shadow: 0 2px 16px rgba(90,79,207,0.04); padding: 40px 32px; margin-bottom: 40px; }}
        .post-content h1, .post-content h2, .post-content h3 {{ color: var(--text-color); margin-top: 1.5em; margin-bottom: 0.7em; }}
        .post-content h1 {{ font-size: 2.1rem; }}
        .post-content h2 {{ font-size: 1.4rem; }}
        .post-content h3 {{ font-size: 1.1rem; }}
        .post-content p {{ margin-bottom: 1.2em; }}
        .post-content ul, .post-content ol {{ margin-left: 1.5em; margin-bottom: 1.2em; }}
        .post-content a {{ color: var(--link-color); text-decoration: none; }}
        .post-content a:hover {{ color: var(--link-hover); text-decoration: underline; }}
        .post-content pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; margin-bottom: 1.2em; }}
        .post-content code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 0.97em; }}
        .post-content img {{ max-width: 100%; border-radius: 8px; margin: 18px 0; display: block; }}
        .post-content blockquote {{ border-left: 3px solid var(--border-color); padding-left: 15px; margin: 18px 0; color: var(--text-muted); background: #faf7f2; }}
        .post-content table {{ border-collapse: collapse; width: 100%; margin-bottom: 1.2em; }}
        .post-content th, .post-content td {{ border: 1px solid #e0d8cc; padding: 8px 12px; }}
        .post-content th {{ background: #f5f0e8; }}
        @media (max-width: 600px) {{ .post-content {{ padding: 18px 6px; }} }}
        footer {{ padding: 40px 0; text-align: center; border-top: 1px solid var(--border-color); margin-top: auto; }}
        footer p {{ color: var(--text-muted); font-size: 0.85rem; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="logo">Miraç</a>
            <nav>
                <a href="/">Blog</a>
                <div class="nav-icons">
                    <a href="https://github.com/AkbulutMirac" target="_blank" title="GitHub">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                        </svg>
                    </a>
                </div>
            </nav>
        </div>
    </header>
    <main>
        <div class="container">
            <div class="divider"></div>
            <article class="post-content">
                {html_content}
            </article>
        </div>
    </main>
    <footer>
        <div class="container">
            <p>© 2026 Mirac. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
    
    return fastapi.Response(content=full_html, media_type="text/html")



@router.post("/post_blog_post_markdown/{slug}/{user_password}")
async def post_blog_post_markdown(slug: str, user_password: str, request: Request, markdown_content: str = None):
    """Adding a new blog post in markdown format (accepts query param or body)"""
    if user_password != CORRECT_PASSWORD:
        return fastapi.Response(status_code=403, content="Yetkisiz erişim - Şifre hatalı")
    # Prioritize getting data according to content-type: JSON first, then form, then explicit param
    content = markdown_content
    title_from_body = None
    ctype = request.headers.get("content-type", "")
    data = None
    try:
        if "application/json" in ctype:
            data = await request.json()
        elif ctype.startswith("application/x-www-form-urlencoded") or ctype.startswith("multipart/form-data"):
            form = await request.form()
            data = dict(form)
    except Exception:
        data = None

    if data:
        if content is None:
            content = data.get("markdown_content")
        title_from_body = data.get("title")
    if content is None or str(content).strip() == "":
        return fastapi.Response(status_code=400, content="İçerik boş olamaz")
    
    
    now = datetime.time().strftime("%Y-%m-%d %H:%M")

    def slugify_py(s: str) -> str:
        if not s:
            return ''
        s = s.lower()
        s = s.replace('_', ' ')
        s = re.sub(r"\s+", '-', s)
        s = re.sub(r"[^a-z0-9-]", '', s)
        s = re.sub(r"-+", '-', s)
        return s.strip('-')

    safe_slug = slugify_py(slug)
    # If safe_slug is empty, try from provided title, else fallback to timestamp
    if not safe_slug:
        safe_slug = slugify_py(title_from_body or slug) or f"post-{int(time.time())}"

    title = (title_from_body or slug.replace('-', ' ')).strip()
    header = f"# {title}\n\n*Eklenme tarihi: {now}*\n\n"
    content = header + content.lstrip()
    file_path = p / f"{safe_slug}.md"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return fastapi.Response(content="Blog yazısı başarıyla kaydedildi!", media_type="text/plain")

@router.delete("/delete_blog_post/{slug}/{user_password}")
def delete_blog_post(slug: str, user_password: str):
    """Delete a blog post by slug"""
    if user_password != CORRECT_PASSWORD:
        return fastapi.Response(status_code=403, content="Yetkisiz erişim - Şifre hatalı")
    file_path = p / f"{slug}.md"
    if not file_path.exists():
        return fastapi.Response(status_code=404, content="Blog yazısı bulunamadı")
    os.remove(file_path)
    return fastapi.Response(content="Blog yazısı başarıyla silindi!", media_type="text/plain")