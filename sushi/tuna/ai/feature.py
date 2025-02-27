from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

# Enum for structured categorization
class Sentiment(Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"

class CTAType(Enum):
    URGENCY = "Urgency"
    INFORMATIVE = "Informative"
    DISCOUNT = "Discount"
    SOCIAL_PROOF = "Social Proof"

# Image Feature Extraction
@dataclass
class ImageFeatures:
    objects_detected: List[str]  # ["food", "people", "car"]
    dominant_colors: List[str]  # ["red", "yellow"]
    brightness: float  # Value between 0-1
    contrast: float  # Value between 0-1
    people_count: int
    emotion_detected: Optional[str] = None  # e.g., "Happy", "Neutral"
    logo_present: bool = False
    text_present: bool = False
    visual_complexity: str = "Minimalistic"  # "Minimalistic", "Moderate", "Cluttered"

# Video Feature Extraction
@dataclass
class VideoFeatures:
    duration: int  # in seconds
    retention_rate: float  # % of users watching till end
    scene_cuts: int  # Number of transitions
    voiceover_present: bool
    background_music_type: Optional[str] = None  # "Upbeat", "Calm", etc.
    subtitle_present: bool = False
    pacing: str = "Medium"  # "Slow", "Medium", "Fast"

# Text Features for Titles & Descriptions
@dataclass
class TextFeatures:
    word_count: int
    readability_score: float  # Flesch-Kincaid score
    contains_numbers: bool
    power_words_used: List[str]  # ["Exclusive", "Limited Time"]
    sentiment: Sentiment
    question_included: bool
    call_to_engagement: bool  # ("Tag a friend", "Comment below")

# CTA Features
@dataclass
class CTAFeatures:
    text: str  # "Buy Now", "Learn More"
    cta_type: CTAType
    position: str  # "Above fold", "Below fold", "Middle of video"
    color_contrast: str  # "High", "Medium", "Low"
    size: str  # "Small", "Medium", "Large"

# Audience & Performance Metrics
@dataclass
class AdPerformance:
    platform: str  # "Facebook", "Google", "TikTok"
    age_group: List[str]  # ["18-24", "25-34"]
    gender_distribution: dict  # {"Male": 60%, "Female": 40%}
    engagement_rate: float  # CTR / Impressions
    conversion_rate: float  # Purchases / Clicks
    best_time_to_post: Optional[str] = None  # e.g., "Evening", "Morning"

# Main Ad Object
@dataclass
class AdContent:
    title: str
    description: str
    image_features: Optional[ImageFeatures] = None
    video_features: Optional[VideoFeatures] = None
    text_features: TextFeatures = field(default_factory=TextFeatures)
    cta_features: CTAFeatures = field(default_factory=CTAFeatures)
    performance: AdPerformance = field(default_factory=AdPerformance)