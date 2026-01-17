import os
import django
os.environ['DATABASE_URL'] = 'postgresql://bol7_user:moDVXCI6moV4t955dR2WRhnpPUVpK6NF@dpg-d5k9feqli9vc73f9long-a.singapore-postgres.render.com/bol7_db'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mysite.models import CompanyDocument
from mysite.utils import text_to_vector, detect_language

# COMPLETE BOL7 DATA (EVERYTHING!)
bol7_data = [
    # === BASIC INFO ===
    "BOL7 Technologies Private Limited is located in New Delhi, India",
    "BOL7 Technologies main office is at A-27J, Noida Sector 16, Gautam Buddha Nagar, Uttar Pradesh 201301",
    "BOL7 was founded on September 29, 2010",
    "BOL7 Technologies is a private limited company incorporated in India",
    "BOL7 is a reputed and quality driven Digital Marketing Company",
    
    # === LEADERSHIP & MANAGEMENT ===
    "Hemant Gupta is the founder, co-founder, director and admin of BOL7 Technologies",
    "Mr. Hemant Gupta founded BOL7 Technologies on September 29, 2010",
    "Pramod Saggar is co-founder and director of BOL7 Technologies",
    "Hemant Gupta and Pramod Saggar are the co-founders of BOL7 Technologies",
    "The founders of BOL7 are Hemant Gupta and Pramod Saggar",
    "Anil is the manager at BOL7 Technologies",
    "Anil manages BOL7 Technologies operations",
    "Priyanka is the supervisor at BOL7 Technologies",
    "Priyanka supervises operations at BOL7",
    "Miss Susmita is associated with BOL7 Technologies",
    "Susmita works at BOL7 Technologies",
    
    # === CONTACT INFORMATION ===
    "BOL7 Technologies contact email is SHASHANK@BOL7.COM",
    "BOL7 email for inquiries is SHASHANK@BOL7.COM",
    "Contact BOL7 via email at SHASHANK@BOL7.COM",
    "BOL7 Technologies HR contact number is +91 70650 40985",
    "BOL7 phone number is +91 70650 40985",
    "Call BOL7 at +91 70650 40985",
    "WhatsApp BOL7 at +91 70650 40985",
    "Hemant Gupta Skype ID is live:hemant_136",
    "For business inquiries, contact SHASHANK@BOL7.COM or call +91 70650 40985",
    
    # === OFFICE & ADDRESS ===
    "BOL7 office location is A-27J, Noida Sector 16",
    "BOL7 complete address: A-27J, Noida Sec 16, Gautam Buddha Nagar, Uttar Pradesh 201301",
    "BOL7 has offices in Noida, Uttar Pradesh",
    "BOL7 Technologies headquarters is in Noida Sector 16",
    "BOL7 is located in Noida, Uttar Pradesh, India",
    
    # === TEAM SIZE ===
    "BOL7 Technologies has a total of 198 employees",
    "Total workforce at BOL7 Technologies is 198 people",
    "BOL7 employs 198 people",
    "BOL7 Technologies has 58 Python developers",
    "Total Python developers at BOL7 is 58",
    "BOL7 Technologies has 17 .NET developers",
    "Total .NET developers at BOL7 is 17",
    "BOL7 employs a dedicated Python development team",
    
    # === TECHNOLOGY STACK ===
    "BOL7 focuses on scalable backend systems using Python and .NET technologies",
    "BOL7 Technologies works on cloud platforms including AWS and Azure",
    "BOL7 follows agile development methodology for project execution",
    
    # === SERVICES (COMPREHENSIVE) ===
    "BOL7 provides digital marketing services including SEO, SEM, and social media management",
    "BOL7 offers software development and custom application development services",
    "BOL7 provides WhatsApp Business API integration services",
    "BOL7 provides WhatsApp Business Cloud API services starting from Rs 1000",
    "BOL7 specializes in AI-powered chatbot and automation solutions",
    "BOL7 builds custom enterprise software for government and private clients",
    "BOL7 Technologies delivers CRM and ERP software solutions",
    "BOL7 Technologies provides IT consulting and digital transformation services",
    "BOL7 offers business automation services and call center solutions",
    "BOL7 provides online reputation management and brand building services",
    "BOL7 offers political campaign management and voter engagement tools",
    "BOL7 Technologies specializes in digital voting systems and election technology",
    "BOL7 provides media buying and influencer marketing services",
    "BOL7 offers cloud hosting and email solutions for businesses",
    "BOL7 provides bulk SMS services for India starting from Rs 0.15 per SMS",
    "BOL7 offers voice broadcasting and OBD services",
    "BOL7 provides IVR services for automated call handling",
    "BOL7 offers RCS messaging services starting from Rs 0.18",
    "BOL7 provides Google Ads services and management",
    "BOL7 offers Facebook and Instagram advertising services",
    "BOL7 provides LinkedIn advertising for B2B lead generation",
    "BOL7 offers X (Twitter) advertising services",
    "BOL7 provides Snapchat advertising services",
    "BOL7 offers B2B lead generation services",
    "BOL7 provides data center colocation services",
    "BOL7 offers logo design and graphics creation services",
    "BOL7 provides video editing services",
    "BOL7 offers article and blog writing services",
    "BOL7 provides OCR data entry services",
    "BOL7 offers email verification and validation services",
    "BOL7 provides WhatsApp number filtration services",
    "BOL7 offers call center dialer software",
    "BOL7 provides political survey services",
    "BOL7 offers link building services for SEO",
    "BOL7 provides website traffic generation services",
    "BOL7 offers customized QR code services",
    "BOL7 provides Telegram ads services",
    "BOL7 offers business email hosting powered by Rediffmail",
    "BOL7 provides WhatsApp account unblocking services",
    "BOL7 offers social media follower purchase services",
    "BOL7 provides AI-powered CRM solutions",
    "BOL7 offers AI sales chatbot services",
    
    # === GOVERNMENT CLIENTS ===
    "BOL7 serves Ministry of Textiles",
    "BOL7 works with Indian Institute of Management IIM",
    "BOL7 provides services to Indian Navy",
    "BOL7 serves Staff Selection Commission SSC",
    "BOL7 works with Vishwakarma Government Engineering College Chandkheda",
    "BOL7 provides services to Education Department Gujarat",
    "BOL7 serves Employees Provident Fund Organization EPFO",
    "BOL7 works with ENGINEERS INDIA Limited",
    "BOL7 provides services to Directorate of Employment and Training",
    "BOL7 serves Oil and Natural Gas Corporation Limited",
    "BOL7 works with Metal Scrap Trade Corporation Limited",
    "BOL7 provides services to National Instructional Media Institute",
    "BOL7 serves government clients including the Indian Navy",
    
    # === PRIVATE CLIENTS ===
    "BOL7 clients include Times of India",
    "BOL7 clients include Hindustan Times",
    "BOL7 serves Apeejay School",
    "BOL7 works with Times Internet Limited",
    "BOL7 provides services to various media houses",
    "BOL7 works with both government and private sector organizations",
    
    # === COMPANY HISTORY ===
    "BOL7 was founded by Mr. Hemant Gupta with a vision to transform the digital landscape",
    "BOL7 started with focus on SEO, SEM, and Social Media Management",
    "Between 2012-2014, BOL7 expanded into application development and software solutions",
    "During 2015-2017, BOL7 built strong relationships with government and private clients",
    "From 2018-2020, BOL7 introduced WhatsApp Business API, Call Center Services, and Digital Marketing",
    "From 2021 to present, BOL7 is recognized as a leader in next-generation digital services",
    
    # === CHATBOT INFO ===
    "This AI chatbot is developed by Badal Chauhan for BOL7 Technologies",
    "Badal Chauhan is a Python and AI developer who created this chatbot",
    "Badal Chauhan developed the AI chatbot for BOL7",
    "Badal Chauhan is the creator of this intelligent chatbot system",
    "The chatbot uses RAG (Retrieval Augmented Generation) architecture",
    "The chatbot uses pgvector extension for vector similarity search",
    "The chatbot uses HNSW algorithm for ultra-fast vector search in PostgreSQL database",
    "This chatbot provides intelligent question answering about BOL7 Technologies",
]

# Clear old data
print("Clearing old data...")
CompanyDocument.objects.all().delete()
print("Old data cleared!\n")

# Add new data
print("Starting to add BOL7 data...\n")

for i, text in enumerate(bol7_data, 1):
    try:
        language = detect_language(text)
        print(f"[{i}/{len(bol7_data)}] Converting: {text[:60]}...")
        vector = text_to_vector(text)
        
        CompanyDocument.objects.create(
            text=text,
            vector=vector,
            metadata={'language': language, 'category': 'company_info'}
        )
        
        print(f"✅ Saved! (Language: {language})\n")
        
    except Exception as e:
        print(f"❌ Failed: {e}\n")

print("🎉 All data added successfully!")
print(f"Total entries: {len(bol7_data)}")