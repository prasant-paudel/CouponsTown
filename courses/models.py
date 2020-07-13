from django.db import models
from multiselectfield import MultiSelectField

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    name_encoded = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200)
    affiliate_url = models.CharField(max_length=256,blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    contents = models.BinaryField(blank=True)
    best_seller = models.BooleanField(null=True)
    expired = models.BooleanField(default=False)
    platform = models.CharField(max_length=30, blank=True)
    duration = models.CharField(blank=True, max_length=10)
    upload_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(max_length=5, blank=True, null=True)
    category_coices = (
        ('not_set', 'NOT SET'),
        ( 'development', 'DEVELOPMENT'),
        ('it&software', 'IT & SOFTWARE'),
        ('office&productivity', 'OFFICE & PRODUCTIVITY'),
        ('design&photography', 'DESIGN & PHOTOGRAPHY'),
        ('marketing&business', 'MARKETING & BUSINESS'),
        ('others', 'OTHERS'),
    )
    category = models.CharField(choices=category_coices, default='not_set', max_length=21)
    # Tags
    tags_choices = (
        ('all_academics', 'All Academics'),
        ('accounting', 'Accounting'),
        ('astrology', 'Astrology'),
        ('chemistry', 'Chemistry'),
        ('engineering', 'Engineering'),
        ('history', 'History'),
        ('management', 'Management'),
        ('math', 'Math'),
        ('physics', 'Physics'),
        ('politics', 'Politics'),
        ('science', 'Science'),
        ('all_business', 'All Business'),
        ('business_law', 'Business Law'),
        ('communications', 'Communications'),
        ('cryptocurrency', 'Cryptocurrency'),
        ('data_&_analytics', 'Data & Analytics'),
        ('e-commerce', 'E-Commerce'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('finance', 'Finance'),
        ('freelance', 'Freelance'),
        ('home_business', 'Home Business'),
        ('human_resources', 'Human Resources'),
        ('media', 'Media'),
        ('personal_brand_building', 'Personal Brand Building'),
        ('personal_finance', 'Personal Finance'),
        ('project_management', 'Project Management'),
        ('real_estate', 'Real Estate'),
        ('sales', 'Sales'),
        ('small_business', 'Small Business'),
        ('start-up', 'Start-up'),
        ('strategy', 'Strategy'),
        ('all_design', 'All Design'),
        ('3d_&_animation', '3D & Animation'),
        ('design_thinking', 'Design Thinking'),
        ('design_tools', 'Design Tools'),
        ('fashion', 'Fashion'),
        ('game_design', 'Game Design'),
        ('graphic_design', 'Graphic Design'),
        ('user_experience', 'User Experience'),
        ('video_design', 'Video Design'),
        ('web_design', 'Web Design'),
        ('all_development', 'All Development'),
        ('databases', 'Databases'),
        ('development_tools', 'Development Tools'),
        ('game_development', 'Game Development'),
        ('mobile_apps', 'Mobile Apps'),
        ('other_programming', 'Other Programming'),
        ('programming_languages', 'Programming Languages'),
        ('web_development', 'Web Development'),
        ('wordpress', 'Wordpress'),
        ('all_health_&_fitness', 'All Health & Fitness'),
        ('dance', 'Dance'),
        ('dieting', 'Dieting'),
        ('fitness', 'Fitness'),
        ('food_&_beverage', 'Food & Beverage'),
        ('general_health', 'General Health'),
        ('mental_health', 'Mental Health'),
        ('nutrition', 'Nutrition'),
        ('safety_&_first_aid', 'Safety & First Aid'),
        ('self_defense', 'Self Defense'),
        ('sports', 'Sports'),
        ('all_it_&_software', 'All IT & Software'),
        ('hardware', 'Hardware'),
        ('it_certification', 'IT Certificatio'),
        ('network_&_security', 'Network & Security'),
        ('operating_systems', 'Operating Systems'),
        ('software_engineering', 'Software Engineering'),
        ('all_languages', 'All Languages'),
        ('arabic', 'Arabic'),
        ('chinese', 'Chinese'),
        ('deutsch', 'Deutsch'),
        ('english', 'English'),
        ('french', 'French'),
        ('german', 'Germ'),
        ('hindi', 'Hindi'),
        ('italian', 'Italian'),
        ('japanese', 'Japanese'),
        ('korean', 'Korean'),
        ('polish', 'Polish'),
        ('romanian', 'Romanian'),
        ('spanish', 'Spanish'),
        ('turkish', 'Turkish'),
        ('vietnamese', 'Vietnamese'),
        ('all_lifestyle', 'All Lifestyle'),
        ('arts_&_crafts', 'Arts & Crafts'),
        ('gaming', 'Gaming'),
        ('home_improvement', 'Home Improvement'),
        ('other', 'Other'),
        ('pet_care_&_training', 'Pet Care & Training'),
        ('travel', 'Travel'),
        ('all_marketing', 'All Marketing'),
        ('advertising', 'Advertising'),
        ('affiliate_marketing', 'Affiliate Marketing'),
        ('analytics_&_automation', 'Analytics & Automatio'),
        ('branding', 'Branding'),
        ('content_marketing', 'Content Marketing'),
        ('digital_marketing', 'Digital Marketing'),
        ('email_marketing', 'Email Marketing'),
        ('growth_hacking', 'Growth Hacking'),
        ('marketing_fundamentals', 'Marketing Fundamentals'),
        ('marketing_tools', 'Marketing Tools'),
        ('non-digital_marketing', 'Non-Digital Marketing'),
        ('online_marketing', 'Online Marketing'),
        ('product_marketing', 'Product Marketing'),
        ('public_relations', 'Public Relations'),
        ('search_engine_optimization', 'Search Engine Optimization'),
        ('social_media_marketing', 'Social Media Marketing'),
        ('video_&_mobile_marketing', 'Video & Mobile Marketing'),
        ('all_music', 'All Music'),
        ('instruments', 'Instruments'),
        ('music_fundamentals', 'Music Fundamentals'),
        ('music_software', 'Music Software'),
        ('music_techniques', 'Music Techniques'),
        ('production', 'Production'),
        ('all_office_productivity', 'All Office Productivity'),
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('salesforce', 'Salesforce'),
        ('all_personal_development', 'All Personal Development'),
        ('career_development', 'Career Development'),
        ('chess', 'Chess'),
        ('creativity', 'Creativity'),
        ('exams_preparation', 'Exams Preparation'),
        ('happiness', 'Happiness'),
        ('influence', 'Influence'),
        ('leadership', 'Leadership'),
        ('memory_&_study_skills', 'Memory & Study Skills'),
        ('motivation', 'Motivation'),
        ('parenting_&_relationships', 'Parenting & Relationships'),
        ('personal_transformation', 'Personal Transformation'),
        ('productivity', 'Productivity'),
        ('religion_&_spirituality', 'Religion & Spirituality'),
        ('self_esteem', 'Self Esteem'),
        ('stress_management', 'Stress Management'),
        ('time_management', 'Time Management'),
        ('writing', 'Writing'),
        ('all_photography', 'All Photography'),
        ('black_&_white', 'Black & White'),
        ('digital_photography', 'Digital Photography'),
        ('landscape', 'Landscap'),
        ('photography_fundamentals', 'Photography Fundamentals'),
        ('photography_tools', 'Photography Tools'),
        ('portraits', 'Portraits'),
        ('wedding_photography', 'Wedding Photography'),
        ('all_teacher_training', 'All Teacher Trainin'),
        ('educational_developmen', 'Educational Developmen'),
        ('instructional_design', 'Instructional Design'),
        ('online_teaching', 'Online Teaching'),
        ('teaching_tools', 'Teaching Tools'),
        ('all_test_preperation', 'All Test Preperation'),
        ('grad_entry_exam', 'Grad Entry Exam'),
        ('test_taking_skills', 'Test Taking Skills'),
        ('development', 'Development'),
        ('web_development', 'Web Development'),
        ('programming_languages', 'Programming Languages'),
        ('web_development', 'Web Development'),
    )
    tags = MultiSelectField(choices=tags_choices, null=True)

    def __str__(self):
        if self.expired:
            return '--Expired-- ' + self.name
        return self.name + ' | ' + self.platform
    
    class Meta:
        ordering = ['platform']
        


class Subscriber(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class RealDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    # title = models.CharField(max_length=200)
    offer = models.CharField(max_length=200, unique=True)
    coupon = models.CharField(max_length=200, blank=True, unique=True)
    platform = models.CharField(max_length=30, blank=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        if self.valid:
            validity = 'Valid'
        else:
            validity = 'Invalid'
        return self.coupon + ' | ' + validity
