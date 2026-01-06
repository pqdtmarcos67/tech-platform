from dataclasses import dataclass

@dataclass
class Meta:
    title: str = ""
    description: str = ""
    canonical: str = ""
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""
    twitter_title: str = ""
    twitter_description: str = ""

def meta_defaults(title: str, description: str, canonical: str = "") -> Meta:
    return Meta(
        title=title,
        description=description,
        canonical=canonical,
        og_title=title,
        og_description=description,
        twitter_title=title,
        twitter_description=description,
    )
