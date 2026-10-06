"""
J.A.R.V.I.S. Skills Manager & On-Demand Context Engine
Inspired by the ECC modular skill harness.
Dynamically discovers, scores, and injects specialized engineering rulebooks into agent workflows.
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("SkillsManager")
logger.setLevel(logging.INFO)

SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")


class Skill:
    def __init__(self, filename: str, title: str, keywords: List[str], content: str):
        self.filename = filename
        self.title = title
        self.keywords = [k.lower().strip() for k in keywords]
        self.content = content

    def match_score(self, query: str) -> float:
        clean_q = query.lower()
        score = 0.0
        # Title match
        if self.title.lower() in clean_q:
            score += 5.0
        # Keyword matches
        for kw in self.keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', clean_q):
                score += 3.0
            elif kw in clean_q:
                score += 1.0
        return score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "title": self.title,
            "keywords": self.keywords,
            "snippet": self.content[:200] + "..." if len(self.content) > 200 else self.content
        }


class SkillsManager:
    """Discovers, caches, and routes engineering skills on demand."""

    _cached_skills: Optional[List[Skill]] = None

    @classmethod
    def load_skills(cls, force_reload: bool = False) -> List[Skill]:
        if cls._cached_skills is not None and not force_reload:
            return cls._cached_skills

        skills: List[Skill] = []
        if not os.path.exists(SKILLS_DIR):
            cls._cached_skills = []
            return []

        for fn in os.listdir(SKILLS_DIR):
            if not fn.endswith(".md"):
                continue
            fpath = os.path.join(SKILLS_DIR, fn)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    text = f.read()

                # Extract title from first markdown header
                title_match = re.search(r'^#\s+Skill:\s*(.+)$', text, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else fn.replace(".md", "").replace("_", " ").title()

                # Extract keywords
                kw_match = re.search(r'keywords:\s*\[(.*?)\]', text, re.IGNORECASE)
                keywords = [k.strip() for k in kw_match.group(1).split(",")] if kw_match else []

                skills.append(Skill(filename=fn, title=title, keywords=keywords, content=text))
            except Exception as e:
                logger.warning(f"Error loading skill file {fn}: {e}")

        cls._cached_skills = skills
        logger.info(f"Loaded {len(skills)} modular skills into J.A.R.V.I.S. Skill Harness.")
        return skills

    @classmethod
    def find_relevant_skills(cls, query: str, top_k: int = 2) -> List[Skill]:
        skills = cls.load_skills()
        scored = [(s.match_score(query), s) for s in skills]
        scored.sort(key=lambda x: x[0], reverse=True)
        # Filter items with non-zero relevance score
        matched = [s for score, s in scored if score > 0]
        if not matched and skills:
            # Default to Python clean code & security standards if no specific match
            default_names = ["python_clean_code.md", "security_standards.md"]
            matched = [s for s in skills if s.filename in default_names]
        return matched[:top_k]

    @classmethod
    def get_skills_prompt_context(cls, query: str, top_k: int = 2) -> str:
        """Formats the top matched skills into compact instructions for agent prompt injection."""
        relevant = cls.find_relevant_skills(query, top_k=top_k)
        if not relevant:
            return ""

        sections = []
        for s in relevant:
            sections.append(f"### SKILL MANUAL: {s.title.upper()}\n{s.content.strip()}")

        context = (
            "====================================================================\n"
            "ACTIVE J.A.R.V.I.S. MODULAR SKILL PROTOCOLS (ON-DEMAND INJECTION)\n"
            "====================================================================\n"
            + "\n\n".join(sections) + "\n"
            "===================================================================="
        )
        return context

    @classmethod
    def list_available_skills(cls) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in cls.load_skills()]
