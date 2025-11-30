"""
Markdown parser for extracting textbook content from Docusaurus markdown files.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import frontmatter


class MarkdownParser:
    """Parser for Docusaurus markdown files."""

    @staticmethod
    def heading_to_anchor(heading: str) -> str:
        """
        Convert a heading to a Docusaurus-compatible anchor.
        
        Docusaurus uses the same algorithm as GitHub:
        - Lowercase
        - Replace spaces with hyphens
        - Remove special characters except hyphens
        
        Args:
            heading: The heading text
            
        Returns:
            URL-safe anchor string
        """
        # Lowercase
        anchor = heading.lower()
        # Replace spaces with hyphens
        anchor = re.sub(r'\s+', '-', anchor)
        # Remove special characters except hyphens and alphanumeric
        anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
        # Remove multiple consecutive hyphens
        anchor = re.sub(r'-+', '-', anchor)
        # Remove leading/trailing hyphens
        anchor = anchor.strip('-')
        return anchor

    @staticmethod
    def parse_file(file_path: Path) -> Dict[str, any]:
        """
        Parse a markdown file and extract metadata and content.

        Args:
            file_path: Path to the markdown file

        Returns:
            Dictionary with metadata and cleaned content
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        metadata = post.metadata
        content = post.content

        # Clean the content
        cleaned_content = MarkdownParser._clean_markdown(content)

        # Extract chapter and section from path
        # Expected structure: book-source/docs/chapter-01/section.md
        parts = file_path.parts
        chapter_dir = None
        for i, part in enumerate(parts):
            if part == "docs" and i + 1 < len(parts):
                chapter_dir = parts[i + 1]
                break

        chapter = chapter_dir if chapter_dir else "unknown"
        section_name = file_path.stem

        # Build page path for Docusaurus
        # First, check if there's a slug in the frontmatter (preferred)
        if "slug" in metadata:
            slug = metadata["slug"]
            # Ensure it starts with /docs
            if slug.startswith("/"):
                page_path = f"/docs{slug}"
            else:
                page_path = f"/docs/{slug}"
        else:
            # Fallback: Convert file path to URL
            # docs/chapter-01/intro.md -> /docs/chapter-01/intro
            if "docs" in parts:
                docs_index = parts.index("docs")
                path_parts = parts[docs_index + 1:]
                # Remove file extension
                path_str = "/".join(path_parts)
                page_path = f"/docs/{path_str.replace('.md', '').replace('.mdx', '')}"
            else:
                page_path = f"/docs/{chapter}/{section_name}"

        return {
            "content": cleaned_content,
            "chapter": chapter,
            "chapter_title": metadata.get("chapter_title", chapter.replace("-", " ").title()),
            "section": section_name,
            "section_title": metadata.get("title", metadata.get("sidebar_label", section_name.replace("-", " ").title())),
            "page_path": page_path,
            "metadata": metadata,
        }

    @staticmethod
    def parse_file_by_sections(file_path: Path) -> List[Dict[str, any]]:
        """
        Parse a markdown file and split by headings (## or ###).
        Each section becomes a separate item with its own anchor.

        Args:
            file_path: Path to the markdown file

        Returns:
            List of dictionaries, one per section, with heading anchor included
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        metadata = post.metadata
        content = post.content

        # Extract chapter and section from path
        parts = file_path.parts
        chapter_dir = None
        for i, part in enumerate(parts):
            if part == "docs" and i + 1 < len(parts):
                chapter_dir = parts[i + 1]
                break

        chapter = chapter_dir if chapter_dir else "unknown"
        section_name = file_path.stem

        # Build base page path for Docusaurus
        if "slug" in metadata:
            slug = metadata["slug"]
            if slug.startswith("/"):
                base_page_path = f"/docs{slug}"
            else:
                base_page_path = f"/docs/{slug}"
        else:
            if "docs" in parts:
                docs_index = parts.index("docs")
                path_parts = parts[docs_index + 1:]
                path_str = "/".join(path_parts)
                base_page_path = f"/docs/{path_str.replace('.md', '').replace('.mdx', '')}"
            else:
                base_page_path = f"/docs/{chapter}/{section_name}"

        # Split content by headings (## or ###)
        # Pattern matches ## or ### at start of line
        heading_pattern = r'^(#{2,3})\s+(.+)$'
        
        sections = []
        current_heading = None
        current_anchor = None
        current_content_lines = []
        
        for line in content.split('\n'):
            match = re.match(heading_pattern, line)
            if match:
                # Save previous section if exists
                if current_content_lines:
                    section_content = '\n'.join(current_content_lines)
                    cleaned = MarkdownParser._clean_markdown(section_content)
                    if cleaned.strip():
                        sections.append({
                            "content": cleaned,
                            "chapter": chapter,
                            "chapter_title": metadata.get("chapter_title", chapter.replace("-", " ").title()),
                            "section": section_name,
                            "section_title": metadata.get("title", metadata.get("sidebar_label", section_name.replace("-", " ").title())),
                            "heading": current_heading,
                            "anchor": current_anchor,
                            "page_path": f"{base_page_path}#{current_anchor}" if current_anchor else base_page_path,
                            "base_page_path": base_page_path,
                            "metadata": metadata,
                        })
                
                # Start new section
                current_heading = match.group(2).strip()
                current_anchor = MarkdownParser.heading_to_anchor(current_heading)
                current_content_lines = [line]  # Include the heading itself for context
            else:
                current_content_lines.append(line)
        
        # Don't forget the last section
        if current_content_lines:
            section_content = '\n'.join(current_content_lines)
            cleaned = MarkdownParser._clean_markdown(section_content)
            if cleaned.strip():
                sections.append({
                    "content": cleaned,
                    "chapter": chapter,
                    "chapter_title": metadata.get("chapter_title", chapter.replace("-", " ").title()),
                    "section": section_name,
                    "section_title": metadata.get("title", metadata.get("sidebar_label", section_name.replace("-", " ").title())),
                    "heading": current_heading,
                    "anchor": current_anchor,
                    "page_path": f"{base_page_path}#{current_anchor}" if current_anchor else base_page_path,
                    "base_page_path": base_page_path,
                    "metadata": metadata,
                })
        
        # If no sections found (no ## or ### headings), return whole file as one section
        if not sections:
            cleaned_content = MarkdownParser._clean_markdown(content)
            sections.append({
                "content": cleaned_content,
                "chapter": chapter,
                "chapter_title": metadata.get("chapter_title", chapter.replace("-", " ").title()),
                "section": section_name,
                "section_title": metadata.get("title", metadata.get("sidebar_label", section_name.replace("-", " ").title())),
                "heading": None,
                "anchor": None,
                "page_path": base_page_path,
                "base_page_path": base_page_path,
                "metadata": metadata,
            })
        
        return sections

    @staticmethod
    def _clean_markdown(content: str) -> str:
        """
        Clean markdown content by removing JSX components, HTML, and code blocks.

        Args:
            content: Raw markdown content

        Returns:
            Cleaned text content
        """
        # Remove JSX/React components
        content = re.sub(r'<[A-Z][^>]*>.*?</[A-Z][^>]*>', '', content, flags=re.DOTALL)
        content = re.sub(r'<[A-Z][^/>]*\s*/>', '', content)

        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        # Remove code blocks (optional - keep for now as they might be relevant)
        # content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

        # Remove inline code formatting but keep content
        content = re.sub(r'`([^`]+)`', r'\1', content)

        # Remove image syntax
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

        # Remove links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

        # Remove markdown headers markers but keep text
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

        # Remove bold/italic markers
        content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^\*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)

        # Remove horizontal rules
        content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)

        # Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        return content
