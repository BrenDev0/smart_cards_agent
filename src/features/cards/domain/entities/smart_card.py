from pydantic import BaseModel, Field
from typing import Optional

class SmartCard(BaseModel):
    name: str = Field(
        description="Person's full name or display name. May be found as: 'name', 'full_name', 'display_name', 'contact_name', 'person', 'client_name'",
        examples=["John Smith", "María García", "Dr. Sarah Johnson"]
    )

    position: str = Field(
        description="Job title, role, or professional position. May be found as: 'position', 'title', 'job_title', 'role', 'occupation', 'job', 'profession'",
        examples=["Software Engineer", "Real Estate Agent", "Marketing Manager"]
    )

    phone: str = Field(
        description="Phone number with or without country code. May be found as: 'phone', 'telephone', 'mobile', 'cell', 'contact_number', 'phone_number'",
        examples=["+1-555-123-4567", "555.123.4567", "(555) 123-4567"]
    )

    email: str = Field(
        description="Valid email address. May be found as: 'email', 'email_address', 'contact_email', 'work_email', 'business_email'",
        examples=["john.smith@company.com", "contact@business.com"]
    )

    facebook: Optional[str] = Field(
        default=None,
        description="Facebook profile or page URL. May be found as: 'facebook', 'facebook_url', 'fb', 'facebook_link', 'facebook_page'",
        examples=[
            "https://www.facebook.com/GiselaGomezBienesRaices",
            "https://facebook.com/username",
            "facebook.com/businesspage"
        ]
    )

    instagram: Optional[str] = Field(
        default=None,
        description="Instagram handle (with or without @) or full URL. May be found as: 'instagram', 'ig', 'instagram_handle', 'instagram_url'",
        examples=["@username", "username", "https://instagram.com/username"]
    )

    tiktok: Optional[str] = Field(
        default=None,
        description="TikTok handle (with or without @) or full URL. May be found as: 'tiktok', 'tiktok_handle', 'tiktok_url', 'tt'",
        examples=["@username", "username", "https://tiktok.com/@username"]
    )

    bio: Optional[str] = Field(
        default=None,
        description="Short biography or description of person/business. May be found as: 'bio', 'description', 'about', 'summary', 'profile', 'details'",
        examples=["Experienced real estate agent specializing in luxury homes"]
    )

    location: Optional[str] = Field(
        default=None,
        description="Geographic location (city, state, country). May be found as: 'location', 'address', 'city', 'region', 'area', 'place'",
        examples=["New York, NY", "London, UK", "Miami, Florida"]
    )

    web: Optional[str] = Field(
        default=None,
        description="Website URL. May be found as: 'website', 'web', 'url', 'homepage', 'site', 'web_url', 'company_website'",
        examples=["https://www.company.com", "www.business.com", "mysite.com"]
    )

    urlYoutube: Optional[str] = Field(
        default=None,
        description="YouTube channel or video URL. May be found as: 'youtube', 'youtube_url', 'youtube_channel', 'yt'",
        examples=["https://youtube.com/c/channelname", "youtube.com/user/username"]
    )