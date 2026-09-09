"""
Seed the database with comprehensive mock e-commerce product data.
Covers: Laptops, Smartphones, Headphones, TVs, Cameras, Tablets
Sources: Amazon, Flipkart, Croma, Reliance Digital
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal
from models.models import Base, Product, ProductListing, Review, PriceHistory
import random
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

PLATFORMS = ["Amazon", "Flipkart", "Croma", "Reliance Digital"]

PRODUCTS_DATA = [
    # ===================== LAPTOPS =====================
    {
        "name": "ASUS ROG Strix G15 (2024) Gaming Laptop",
        "brand": "ASUS",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "description": "High-performance gaming laptop with AMD Ryzen 9 processor, dedicated NVIDIA RTX 4070 GPU, 16GB DDR5 RAM, and 1TB NVMe SSD. Features 165Hz QHD display and per-key RGB keyboard.",
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400",
        "specifications": {
            "Processor": "AMD Ryzen 9 7945HX",
            "RAM": "16GB DDR5",
            "Storage": "1TB NVMe SSD",
            "GPU": "NVIDIA RTX 4070 8GB",
            "Display": "15.6\" QHD 165Hz",
            "OS": "Windows 11 Home",
            "Battery": "90Whr",
            "Weight": "2.3kg",
            "Ports": "USB-A x3, USB-C, HDMI 2.1, SD Card",
            "WiFi": "WiFi 6E"
        },
        "listings": [
            {"platform": "Amazon", "price": 129990, "original_price": 149990, "discount": 13, "seller": "ASUS Official", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 127999, "original_price": 149990, "discount": 15, "seller": "RetailNet", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
            {"platform": "Croma", "price": 131000, "original_price": 149990, "discount": 13, "seller": "Croma", "availability": "in_stock", "delivery": "Same-day delivery available"},
            {"platform": "Reliance Digital", "price": 128500, "original_price": 149990, "discount": 14, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 3 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Rahul Sharma", "rating": 4.5, "title": "Excellent gaming performance!", "body": "The RTX 4070 handles every game I throw at it. Cyberpunk 2077 runs at 80fps on ultra settings. The 165Hz display is buttery smooth. Build quality is top-notch. Battery life is decent at 3-4 hours for light tasks. Gets warm during heavy gaming but the cooling system keeps it stable.", "verified": True, "helpful": 89, "date": "2024-03-15"},
            {"platform": "Flipkart", "name": "Priya K", "rating": 4.0, "title": "Great laptop but heavy", "body": "Performance is incredible for the price. The keyboard feels premium. However, at 2.3kg it's not the most portable. The fan noise during gaming is quite loud. Display colors are vivid and accurate. Would recommend for serious gamers who don't mind the weight.", "verified": True, "helpful": 67, "date": "2024-02-20"},
            {"platform": "Amazon", "name": "Deepak M", "rating": 5.0, "title": "Best gaming laptop under 1.3L", "body": "Coming from a 5-year-old laptop, this is a revelation. The Ryzen 9 handles my video editing and gaming without breaking a sweat. SSD speeds are blazing fast. The RGB lighting is a nice touch. Highly recommend!", "verified": True, "helpful": 112, "date": "2024-01-10"},
            {"platform": "Croma", "name": "Anjali R", "rating": 3.5, "title": "Good but has minor issues", "body": "Performance is excellent but I faced WiFi connectivity issues initially. Customer support resolved it via driver update. The display has slight backlight bleed at corners. Overall good value for money considering the specs.", "verified": False, "helpful": 34, "date": "2024-03-01"},
            {"platform": "Flipkart", "name": "Vikram S", "rating": 4.5, "title": "Superb for game dev and gaming", "body": "As a game developer, I need both CPU and GPU power. This machine delivers. Unity and Unreal Engine compile times are significantly faster than my old machine. The QHD display helps with detailed work. Thermally it stays around 85C under load which is acceptable.", "verified": True, "helpful": 78, "date": "2024-03-22"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [149990, 149990, 145000, 142000, 138000, 135000, 132000, 130000, 129990]},
            {"platform": "Flipkart", "prices_30days": [149990, 147000, 144000, 140000, 137000, 133000, 130000, 128000, 127999]},
        ]
    },
    {
        "name": "Lenovo IdeaPad Slim 5 (2024)",
        "brand": "Lenovo",
        "category": "Laptops",
        "subcategory": "Ultrabooks",
        "description": "Slim and powerful ultrabook with Intel Core i7 processor, 16GB RAM, 512GB SSD. Perfect for students and professionals with 12-hour battery life.",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400",
        "specifications": {
            "Processor": "Intel Core i7-13700H",
            "RAM": "16GB LPDDR5",
            "Storage": "512GB NVMe SSD",
            "GPU": "Intel Iris Xe Graphics",
            "Display": "15.6\" FHD IPS 300nits",
            "OS": "Windows 11 Home",
            "Battery": "57Whr (12hrs)",
            "Weight": "1.7kg",
            "Ports": "USB-A x2, USB-C, HDMI, SD Card",
            "WiFi": "WiFi 6"
        },
        "listings": [
            {"platform": "Amazon", "price": 64990, "original_price": 79990, "discount": 19, "seller": "Lenovo Official", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 62999, "original_price": 79990, "discount": 21, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 67000, "original_price": 79990, "discount": 16, "seller": "Croma", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Reliance Digital", "price": 65500, "original_price": 79990, "discount": 18, "seller": "Reliance Digital", "availability": "limited_stock", "delivery": "Free delivery in 4 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Sonia T", "rating": 4.5, "title": "Perfect college laptop", "body": "As a CSE student this is exactly what I needed. Handles coding, browsing, and light gaming with ease. The battery easily lasts a full day of college. Build quality is solid for the price. The keyboard is comfortable for long typing sessions.", "verified": True, "helpful": 156, "date": "2024-03-10"},
            {"platform": "Flipkart", "name": "Arun P", "rating": 4.0, "title": "Good value for money", "body": "Solid everyday laptop. Fast boot times, responsive performance. Not for gaming beyond casual titles. The display is decent but not the most color-accurate. Webcam quality is average. Overall highly recommended for students and professionals.", "verified": True, "helpful": 98, "date": "2024-02-14"},
            {"platform": "Amazon", "name": "Meera B", "rating": 3.5, "title": "Good but expected better display", "body": "Performance is great but the 300nit display is a bit dim outdoors. For indoor use it's fine. RAM and storage are sufficient. Battery life is as advertised at 10-12 hours of mixed use. Would be perfect with a brighter display.", "verified": True, "helpful": 45, "date": "2024-01-28"},
            {"platform": "Croma", "name": "Rajan K", "rating": 5.0, "title": "Lightweight and fast", "body": "At 1.7kg this is very portable. Carry it daily without feeling the weight. The i7 handles my office work - Excel, Word, Teams, multiple browser tabs without any lag. Best ultrabook in this price range.", "verified": True, "helpful": 67, "date": "2024-03-05"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [79990, 76000, 73000, 70000, 68000, 66000, 65000, 64990, 64990]},
            {"platform": "Flipkart", "prices_30days": [79990, 75000, 71000, 68000, 66000, 64000, 63000, 62999, 62999]},
        ]
    },
    {
        "name": "HP Omen 16 (2024) Gaming Laptop",
        "brand": "HP",
        "category": "Laptops",
        "subcategory": "Gaming Laptops",
        "description": "Powerful gaming laptop with Intel Core i7, RTX 4060, 16GB RAM, 512GB SSD. Features OMEN Tempest cooling and 144Hz QHD display.",
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400",
        "specifications": {
            "Processor": "Intel Core i7-13700HX",
            "RAM": "16GB DDR5",
            "Storage": "512GB NVMe SSD",
            "GPU": "NVIDIA RTX 4060 8GB",
            "Display": "16.1\" QHD 144Hz IPS",
            "OS": "Windows 11 Home",
            "Battery": "83Whr",
            "Weight": "2.4kg",
            "Ports": "USB-A x3, USB-C Thunderbolt 4, HDMI 2.1",
            "WiFi": "WiFi 6E"
        },
        "listings": [
            {"platform": "Amazon", "price": 89990, "original_price": 109990, "discount": 18, "seller": "HP Official India", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 87999, "original_price": 109990, "discount": 20, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 91000, "original_price": 109990, "discount": 17, "seller": "Croma", "availability": "in_stock", "delivery": "Free delivery in 3 days"},
            {"platform": "Reliance Digital", "price": 90000, "original_price": 109990, "discount": 18, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Kartik V", "rating": 4.5, "title": "Amazing gaming performance!", "body": "RTX 4060 is perfect for 1080p gaming. Plays Valorant at 200+ fps, GTA V maxed out at 60fps. The cooling is excellent, temperatures stay manageable. Display is gorgeous with QHD and 144Hz. Battery is decent at 3 hours gaming. Very satisfied.", "verified": True, "helpful": 134, "date": "2024-03-18"},
            {"platform": "Flipkart", "name": "Neha S", "rating": 4.0, "title": "Great performance, average build", "body": "Performance is top-notch for the price. However, the plastic lid feels a bit cheap compared to ASUS ROG. Keyboard is comfortable. The 144Hz display is smooth. Thermal management is good. Would have preferred an all-metal build at this price.", "verified": True, "helpful": 87, "date": "2024-02-25"},
            {"platform": "Amazon", "name": "Suresh M", "rating": 5.0, "title": "Best value gaming laptop!", "body": "After comparing 5 laptops in this range, HP Omen 16 wins on value. RTX 4060 performs better than expected. Thunderbolt 4 is a bonus. Setup was straightforward, no bloatware issues. Runs cool even after hours of gaming. Highly recommended!", "verified": True, "helpful": 201, "date": "2024-01-15"},
            {"platform": "Croma", "name": "Pooja G", "rating": 3.5, "title": "Loud fan but great performance", "body": "The fans get quite loud during gaming. Performance is excellent but the noise might bother you in quiet environments. Display is beautiful. Build quality is okay. Good laptop overall if you can tolerate fan noise.", "verified": False, "helpful": 29, "date": "2024-03-10"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [109990, 104000, 99000, 95000, 92000, 91000, 90000, 89990, 89990]},
            {"platform": "Flipkart", "prices_30days": [109990, 102000, 97000, 93000, 90000, 89000, 88000, 87999, 87999]},
        ]
    },
    {
        "name": "Dell XPS 15 (2024)",
        "brand": "Dell",
        "category": "Laptops",
        "subcategory": "Premium Ultrabooks",
        "description": "Premium ultrabook with Intel Core i9, 32GB RAM, 1TB SSD, NVIDIA RTX 4060, and stunning 3.5K OLED display. Professional-grade build quality.",
        "image_url": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400",
        "specifications": {
            "Processor": "Intel Core i9-13900H",
            "RAM": "32GB LPDDR5",
            "Storage": "1TB NVMe SSD",
            "GPU": "NVIDIA RTX 4060 8GB",
            "Display": "15.6\" 3.5K OLED Touch 120Hz",
            "OS": "Windows 11 Pro",
            "Battery": "86Whr (10hrs)",
            "Weight": "1.86kg",
            "Ports": "Thunderbolt 4 x2, USB-C, SD Card",
            "WiFi": "WiFi 6E + Bluetooth 5.3"
        },
        "listings": [
            {"platform": "Amazon", "price": 189990, "original_price": 219990, "discount": 14, "seller": "Dell Official", "availability": "in_stock", "delivery": "Free delivery in 3 days"},
            {"platform": "Flipkart", "price": 185999, "original_price": 219990, "discount": 15, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Croma", "price": 192000, "original_price": 219990, "discount": 13, "seller": "Croma", "availability": "limited_stock", "delivery": "Free delivery in 4 days"},
            {"platform": "Reliance Digital", "price": 188000, "original_price": 219990, "discount": 14, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 3 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Arnav D", "rating": 5.0, "title": "The OLED display is breathtaking", "body": "The 3.5K OLED display is simply stunning - perfect blacks, incredible color accuracy. As a photographer and designer, this is everything I need. Performance with i9 and RTX 4060 is exceptional. Build quality is premium. Battery lasts 8-10 hours for creative work. Worth every rupee.", "verified": True, "helpful": 267, "date": "2024-03-20"},
            {"platform": "Flipkart", "name": "Swati N", "rating": 4.5, "title": "Premium but limited ports", "body": "Excellent machine in every way - performance, display, build. The only downside is limited ports (only Thunderbolt 4 and USB-C). You'll need a hub. OLED display has slight burn-in risk if static content is displayed for long. Everything else is perfect.", "verified": True, "helpful": 143, "date": "2024-02-08"},
            {"platform": "Amazon", "name": "Harsh P", "rating": 4.0, "title": "Great laptop, expensive but worth it", "body": "For professionals the XPS 15 justifies its price. i9 handles video editing in 4K without any hiccups. The OLED display helps with color grading. Fan noise is controlled. Thermal throttling not observed in everyday professional tasks. Build is solid aluminum.", "verified": True, "helpful": 89, "date": "2024-01-30"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [219990, 215000, 210000, 205000, 200000, 196000, 193000, 190000, 189990]},
            {"platform": "Flipkart", "prices_30days": [219990, 213000, 207000, 202000, 198000, 194000, 190000, 186000, 185999]},
        ]
    },
    {
        "name": "Acer Aspire Lite (2024)",
        "brand": "Acer",
        "category": "Laptops",
        "subcategory": "Budget Laptops",
        "description": "Budget-friendly laptop for students and professionals. Intel Core i5, 8GB RAM, 512GB SSD with 10-hour battery life.",
        "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400",
        "specifications": {
            "Processor": "Intel Core i5-1235U",
            "RAM": "8GB LPDDR4X",
            "Storage": "512GB NVMe SSD",
            "GPU": "Intel UHD Graphics",
            "Display": "15.6\" FHD IPS",
            "OS": "Windows 11 Home",
            "Battery": "50Whr (10hrs)",
            "Weight": "1.6kg",
            "Ports": "USB-A x2, USB-C, HDMI, SD Card",
            "WiFi": "WiFi 5"
        },
        "listings": [
            {"platform": "Amazon", "price": 38990, "original_price": 49990, "discount": 22, "seller": "Acer Official", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 37499, "original_price": 49990, "discount": 25, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 40000, "original_price": 49990, "discount": 20, "seller": "Croma", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Riya S", "rating": 4.0, "title": "Great budget laptop!", "body": "For under 40k this is unbeatable. Handles all my college work - coding in VS Code, browsing, Office apps. The SSD makes it snappy. Battery lasts a full day. Build quality is decent. Not for gaming but excellent for students.", "verified": True, "helpful": 234, "date": "2024-03-12"},
            {"platform": "Flipkart", "name": "Om T", "rating": 3.5, "title": "Good for basics, average display", "body": "Does the job for everyday tasks. The display lacks brightness and color accuracy. RAM is on the lower side - felt lag with too many browser tabs open. Would upgrade to 16GB version if budget allows. Overall decent for the price.", "verified": True, "helpful": 112, "date": "2024-02-18"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [49990, 47000, 45000, 43000, 41000, 40000, 39000, 38990, 38990]},
            {"platform": "Flipkart", "prices_30days": [49990, 46000, 44000, 42000, 40000, 39000, 38000, 37499, 37499]},
        ]
    },
    # ===================== SMARTPHONES =====================
    {
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "category": "Smartphones",
        "subcategory": "Flagship Phones",
        "description": "Samsung's top flagship with Snapdragon 8 Gen 3, 200MP camera, built-in S Pen, 12GB RAM, and titanium frame. The ultimate Android flagship.",
        "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400",
        "specifications": {
            "Processor": "Snapdragon 8 Gen 3",
            "RAM": "12GB",
            "Storage": "256GB",
            "Main Camera": "200MP f/1.7",
            "Front Camera": "12MP",
            "Display": "6.8\" QHD+ Dynamic AMOLED 120Hz",
            "Battery": "5000mAh, 45W charging",
            "OS": "Android 14, One UI 6.1",
            "5G": "Yes",
            "Special": "S Pen included, IP68, Titanium frame"
        },
        "listings": [
            {"platform": "Amazon", "price": 129999, "original_price": 134999, "discount": 4, "seller": "Samsung India", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
            {"platform": "Flipkart", "price": 128999, "original_price": 134999, "discount": 4, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 131000, "original_price": 134999, "discount": 3, "seller": "Croma", "availability": "in_stock", "delivery": "Same-day delivery"},
            {"platform": "Reliance Digital", "price": 130000, "original_price": 134999, "discount": 4, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Kiran A", "rating": 5.0, "title": "The S Pen is a game changer!", "body": "Using the S Pen for note-taking and sketching is fantastic. The 200MP camera captures insane detail. Night mode is best-in-class. The titanium frame feels incredibly premium. Battery lasts easily 2 days with moderate use. One UI is clean and feature-packed. Best Android phone money can buy.", "verified": True, "helpful": 456, "date": "2024-03-25"},
            {"platform": "Flipkart", "name": "Shreya K", "rating": 4.5, "title": "Excellent camera, premium feel", "body": "Camera quality is unmatched. The 200MP main sensor with optical zoom produces professional quality shots. Display is gorgeous. S Pen adds unique productivity features. Only downside is the size - it's huge. Not great for one-handed use. Battery life is solid.", "verified": True, "helpful": 312, "date": "2024-02-15"},
            {"platform": "Amazon", "name": "Raj P", "rating": 4.0, "title": "Great flagship but pricey", "body": "For ₹1.3L you get the best Android experience. Everything about this phone screams premium - materials, display, camera. Samsung DeX is great for productivity. The price is high but justified by the feature set. Would recommend if budget is not a constraint.", "verified": True, "helpful": 178, "date": "2024-01-20"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [134999, 134999, 133000, 132000, 131000, 130000, 130000, 129999, 129999]},
            {"platform": "Flipkart", "prices_30days": [134999, 134999, 132000, 131000, 130000, 129500, 129000, 128999, 128999]},
        ]
    },
    {
        "name": "OnePlus 12 5G",
        "brand": "OnePlus",
        "category": "Smartphones",
        "subcategory": "Flagship Phones",
        "description": "Snapdragon 8 Gen 3, 50MP Hasselblad camera, 100W fast charging, 5400mAh battery, 6.82\" LTPO AMOLED display.",
        "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400",
        "specifications": {
            "Processor": "Snapdragon 8 Gen 3",
            "RAM": "12GB LPDDR5X",
            "Storage": "256GB UFS 4.0",
            "Main Camera": "50MP Hasselblad (Main+Telephoto+Ultra-wide)",
            "Front Camera": "32MP",
            "Display": "6.82\" QHD+ LTPO AMOLED 120Hz",
            "Battery": "5400mAh, 100W SuperVOOC",
            "OS": "Android 14, OxygenOS 14",
            "5G": "Yes",
            "Special": "Alert Slider, IP65"
        },
        "listings": [
            {"platform": "Amazon", "price": 64999, "original_price": 69999, "discount": 7, "seller": "OnePlus India", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
            {"platform": "Flipkart", "price": 63999, "original_price": 69999, "discount": 9, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Reliance Digital", "price": 65000, "original_price": 69999, "discount": 7, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Aarav J", "rating": 5.0, "title": "100W charging is insane!", "body": "Charges from 0 to 100% in just 26 minutes. The Snapdragon 8 Gen 3 is lightning fast. Hasselblad camera tuning makes photos look natural and professional. OxygenOS 14 is clean without excessive bloatware. Display is gorgeous. Best value flagship in India right now!", "verified": True, "helpful": 389, "date": "2024-03-28"},
            {"platform": "Flipkart", "name": "Divya L", "rating": 4.5, "title": "Exceptional performance and battery", "body": "Gaming performance is excellent - BGMI runs at max settings without overheating. Battery easily lasts 1.5 days. The 100W charging means I never worry about battery. Camera produces excellent shots, though Samsung's color science is different. Alert slider is a useful feature I miss on other phones.", "verified": True, "helpful": 267, "date": "2024-02-22"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [69999, 68000, 67000, 66000, 65500, 65000, 65000, 64999, 64999]},
            {"platform": "Flipkart", "prices_30days": [69999, 68000, 67000, 65500, 65000, 64500, 64000, 63999, 63999]},
        ]
    },
    {
        "name": "Apple iPhone 15 Pro",
        "brand": "Apple",
        "category": "Smartphones",
        "subcategory": "Flagship Phones",
        "description": "Apple's latest Pro iPhone with A17 Pro chip, 48MP camera system, titanium design, Action Button, and USB-C with USB3 speeds.",
        "image_url": "https://images.unsplash.com/photo-1592286927505-1def25115558?w=400",
        "specifications": {
            "Processor": "Apple A17 Pro",
            "RAM": "8GB",
            "Storage": "256GB",
            "Main Camera": "48MP Main + 12MP Ultra-wide + 12MP 3x Telephoto",
            "Front Camera": "12MP TrueDepth",
            "Display": "6.1\" Super Retina XDR OLED ProMotion 120Hz",
            "Battery": "3274mAh, 27W charging",
            "OS": "iOS 17",
            "5G": "Yes",
            "Special": "Titanium frame, Action Button, USB-C USB3"
        },
        "listings": [
            {"platform": "Amazon", "price": 134900, "original_price": 134900, "discount": 0, "seller": "Apple India", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
            {"platform": "Flipkart", "price": 132999, "original_price": 134900, "discount": 1, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 134900, "original_price": 134900, "discount": 0, "seller": "Croma", "availability": "in_stock", "delivery": "Same-day delivery"},
            {"platform": "Reliance Digital", "price": 133000, "original_price": 134900, "discount": 1, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Tanya R", "rating": 5.0, "title": "The best iPhone ever made", "body": "A17 Pro is incredibly fast. Camera quality is simply the best I've ever used on a phone. 4K Prores recording is a professional videographer's dream. Build quality with titanium is premium. iOS 17 features are polished. The Action Button adds useful customization. Battery life has improved vs Pro Max.", "verified": True, "helpful": 523, "date": "2024-03-30"},
            {"platform": "Flipkart", "name": "Nikhil M", "rating": 4.5, "title": "Premium but worth it for creators", "body": "If you're in the Apple ecosystem this is the best iPhone to get. The computational photography is outstanding. USB-C is finally here and the USB3 speeds are great for offloading ProRes footage. Build quality feels absolutely premium. Battery could be better but charges faster than before.", "verified": True, "helpful": 298, "date": "2024-02-18"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [134900, 134900, 134900, 134900, 134900, 134900, 134900, 134900, 134900]},
            {"platform": "Flipkart", "prices_30days": [134900, 134500, 133999, 133500, 133000, 133000, 132999, 132999, 132999]},
        ]
    },
    {
        "name": "Redmi Note 13 Pro+ 5G",
        "brand": "Xiaomi",
        "category": "Smartphones",
        "subcategory": "Mid-range Phones",
        "description": "200MP camera, Dimensity 7200 Ultra, 120W HyperCharge, curved AMOLED display. Exceptional mid-range value.",
        "image_url": "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400",
        "specifications": {
            "Processor": "MediaTek Dimensity 7200 Ultra",
            "RAM": "12GB LPDDR5",
            "Storage": "256GB UFS 3.1",
            "Main Camera": "200MP OIS + 8MP Ultra-wide + 2MP Macro",
            "Front Camera": "16MP",
            "Display": "6.67\" FHD+ Curved AMOLED 120Hz",
            "Battery": "5000mAh, 120W HyperCharge",
            "OS": "Android 13, HyperOS",
            "5G": "Yes",
            "Special": "IP68, Curved glass display"
        },
        "listings": [
            {"platform": "Amazon", "price": 31999, "original_price": 36999, "discount": 14, "seller": "Xiaomi India", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 31499, "original_price": 36999, "discount": 15, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Vivek S", "rating": 4.5, "title": "200MP camera is insane for the price!", "body": "Camera quality rivals phones twice the price. 200MP captures incredible detail. Night mode is excellent. 120W charging fills it in 20 minutes. Display is gorgeous with curved edges. HyperOS feels smooth. Best phone under 35k hands down!", "verified": True, "helpful": 445, "date": "2024-03-15"},
            {"platform": "Flipkart", "name": "Pooja T", "rating": 4.0, "title": "Excellent value, minor bloatware", "body": "Phenomenal camera and charging speed. HyperOS has some bloatware apps but manageable. Gaming performance is good - Genshin Impact runs well. Battery lasts all day. The IP68 rating gives peace of mind. Great buy for price-conscious buyers.", "verified": True, "helpful": 312, "date": "2024-02-28"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [36999, 35000, 34000, 33500, 33000, 32500, 32000, 31999, 31999]},
            {"platform": "Flipkart", "prices_30days": [36999, 35000, 34000, 33000, 32500, 32000, 31500, 31499, 31499]},
        ]
    },
    # ===================== HEADPHONES =====================
    {
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "brand": "Sony",
        "category": "Headphones",
        "subcategory": "Over-ear Headphones",
        "description": "Industry-leading noise cancellation with 8 microphones, 30-hour battery, LDAC codec, and multipoint connection. The gold standard for noise-cancelling headphones.",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "specifications": {
            "Type": "Over-ear, Closed-back",
            "Driver": "30mm dynamic driver",
            "Frequency Response": "4Hz - 40,000Hz",
            "Noise Cancellation": "8-mic Integrated Processor V1",
            "Connectivity": "Bluetooth 5.2, LDAC, AAC, SBC",
            "Battery": "30 hours ANC on, 40 hours ANC off",
            "Quick Charge": "3-min charge = 3 hours playback",
            "Weight": "250g",
            "Foldable": "No",
            "Mic": "Yes, call quality microphone"
        },
        "listings": [
            {"platform": "Amazon", "price": 26990, "original_price": 34990, "discount": 23, "seller": "Sony India", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 25999, "original_price": 34990, "discount": 26, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 27500, "original_price": 34990, "discount": 21, "seller": "Croma", "availability": "in_stock", "delivery": "Same-day delivery"},
            {"platform": "Reliance Digital", "price": 27000, "original_price": 34990, "discount": 23, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Maya S", "rating": 5.0, "title": "Best ANC headphones period!", "body": "The noise cancellation on XM5 is absolutely magical. In a noisy cafe, I can hear absolutely nothing except my music. Sound quality is rich, warm, and detailed. 30 hours battery is more than enough for a week of daily commute. Speak-to-Chat feature is genius. Comfortable for long sessions. Worth every rupee.", "verified": True, "helpful": 678, "date": "2024-03-22"},
            {"platform": "Flipkart", "name": "Alok B", "rating": 4.5, "title": "Exceptional for work-from-home", "body": "These have transformed my WFH experience. Background noise from AC, traffic, family disappears instantly. Call quality is crystal clear - colleagues say I sound better. Sound signature is balanced and pleasing. Multipoint connection between laptop and phone works flawlessly.", "verified": True, "helpful": 456, "date": "2024-02-10"},
            {"platform": "Amazon", "name": "Preethi V", "rating": 4.0, "title": "Amazing headphones but not foldable", "body": "Sound quality and ANC are best in class. Battery life is exceptional. The only complaint is they don't fold flat like XM4 - makes them slightly less portable. The carrying case is smaller though. Comfort is excellent even after 3-4 hours of continuous use.", "verified": True, "helpful": 234, "date": "2024-01-05"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [34990, 33000, 31000, 30000, 29000, 28000, 27500, 27000, 26990]},
            {"platform": "Flipkart", "prices_30days": [34990, 32000, 30000, 29000, 28000, 27000, 26500, 26000, 25999]},
        ]
    },
    {
        "name": "Apple AirPods Pro (2nd Generation)",
        "brand": "Apple",
        "category": "Headphones",
        "subcategory": "True Wireless Earbuds",
        "description": "Active Noise Cancellation with Transparency mode, Adaptive Audio, Personalized Spatial Audio, and MagSafe charging case with 30-hour total battery.",
        "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",
        "specifications": {
            "Type": "In-ear, True Wireless",
            "Chip": "Apple H2",
            "ANC": "Adaptive Active Noise Cancellation",
            "New Feature": "Adaptive Audio, Personalized Spatial Audio",
            "Battery": "6hr earbuds + 24hr case = 30hr total",
            "Water Resistance": "IPX4 earbuds, IPX4 case",
            "Connectivity": "Bluetooth 5.3",
            "Charging": "MagSafe, Lightning, Qi",
            "Find My": "Yes with Precision Finding",
            "Compatibility": "Best with iPhone/iPad/Mac"
        },
        "listings": [
            {"platform": "Amazon", "price": 24900, "original_price": 26900, "discount": 7, "seller": "Apple India", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
            {"platform": "Flipkart", "price": 23999, "original_price": 26900, "discount": 11, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 25900, "original_price": 26900, "discount": 4, "seller": "Croma", "availability": "in_stock", "delivery": "Same-day delivery"},
            {"platform": "Reliance Digital", "price": 24500, "original_price": 26900, "discount": 9, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Siddharth K", "rating": 4.5, "title": "Best earbuds for iPhone users", "body": "If you have an iPhone, AirPods Pro 2 are a no-brainer. The H2 chip makes ANC and Transparency exceptional. Personalized Spatial Audio with head tracking is mind-blowing. Sound quality is excellent. Battery life with case gives me a week of use. The new stem pinch gestures work perfectly.", "verified": True, "helpful": 567, "date": "2024-03-25"},
            {"platform": "Flipkart", "name": "Ananya G", "rating": 4.0, "title": "Great but limited to Apple ecosystem", "body": "Excellent earbuds within the Apple ecosystem. ANC is top-notch. The adaptive audio mode that automatically switches between ANC and transparency based on surroundings is brilliant. Sound quality could be slightly bassier but overall balanced. Pricey for non-Apple users.", "verified": True, "helpful": 345, "date": "2024-02-14"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [26900, 26900, 26500, 26000, 25500, 25000, 25000, 24900, 24900]},
            {"platform": "Flipkart", "prices_30days": [26900, 26500, 25900, 25500, 25000, 24500, 24000, 23999, 23999]},
        ]
    },
    # ===================== TVs =====================
    {
        "name": "Samsung 65\" 4K QLED Smart TV (QN90C)",
        "brand": "Samsung",
        "category": "TVs",
        "subcategory": "QLED TVs",
        "description": "Neo QLED 4K TV with Quantum Matrix Technology Pro, 4K AI Upscaling, 144Hz gaming display, and built-in Alexa.",
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?w=400",
        "specifications": {
            "Screen Size": "65 inches",
            "Resolution": "4K UHD (3840x2160)",
            "Panel": "Neo QLED",
            "Refresh Rate": "144Hz",
            "HDR": "Quantum HDR 32X",
            "Smart TV": "Tizen OS",
            "Connectivity": "HDMI 2.1 x4, USB x3, Bluetooth, WiFi",
            "Gaming": "Gaming Hub, FreeSync Premium Pro, VRR",
            "Sound": "60W Object Tracking Sound+",
            "Special": "AI Upscaling, Auto Game Mode"
        },
        "listings": [
            {"platform": "Amazon", "price": 129990, "original_price": 169990, "discount": 24, "seller": "Samsung India", "availability": "in_stock", "delivery": "Free installation"},
            {"platform": "Flipkart", "price": 125999, "original_price": 169990, "discount": 26, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free installation"},
            {"platform": "Croma", "price": 132000, "original_price": 169990, "discount": 22, "seller": "Croma", "availability": "in_stock", "delivery": "Free installation, demo"},
            {"platform": "Reliance Digital", "price": 128000, "original_price": 169990, "discount": 25, "seller": "Reliance Digital", "availability": "in_stock", "delivery": "Free installation"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Sachin M", "rating": 4.5, "title": "Stunning picture quality!", "body": "The Neo QLED panel produces incredible HDR with deep blacks and brilliant highlights. 4K content looks reference-quality. For gaming, the 144Hz + VRR on PS5 is transformative. The 4K AI Upscaling works surprisingly well on older content. Sound from the built-in speakers is adequate but add a soundbar for the full experience.", "verified": True, "helpful": 345, "date": "2024-03-20"},
            {"platform": "Flipkart", "name": "Rekha P", "rating": 4.0, "title": "Great TV but complex menu system", "body": "Picture quality is excellent. The Tizen OS is feature-rich but takes some getting used to. Smart features work well. The no-gap wall mount is a great optional add-on. 144Hz gaming is exceptional for competitive titles. Worth the investment for a living room centerpiece.", "verified": True, "helpful": 178, "date": "2024-02-12"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [169990, 160000, 155000, 149000, 144000, 138000, 134000, 130000, 129990]},
            {"platform": "Flipkart", "prices_30days": [169990, 158000, 152000, 146000, 141000, 136000, 131000, 127000, 125999]},
        ]
    },
    # ===================== TABLETS =====================
    {
        "name": "Apple iPad Air (M2, 2024)",
        "brand": "Apple",
        "category": "Tablets",
        "subcategory": "Premium Tablets",
        "description": "Powered by M2 chip, 11\" Liquid Retina display, Apple Pencil Pro support, Magic Keyboard support. Perfect for productivity and creativity.",
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
        "specifications": {
            "Chip": "Apple M2",
            "RAM": "8GB",
            "Storage": "256GB",
            "Display": "11\" Liquid Retina 2360x1640 500nits",
            "Cameras": "12MP rear, 12MP front ultrawide",
            "Connectivity": "WiFi 6E, Bluetooth 5.3, USB-C USB3",
            "Battery": "28.65Whr (10 hours)",
            "Accessories": "Apple Pencil Pro, Magic Keyboard",
            "OS": "iPadOS 17",
            "5G": "Optional"
        },
        "listings": [
            {"platform": "Amazon", "price": 74900, "original_price": 74900, "discount": 0, "seller": "Apple India", "availability": "in_stock", "delivery": "Free delivery in 1 day"},
            {"platform": "Flipkart", "price": 72999, "original_price": 74900, "discount": 3, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 74900, "original_price": 74900, "discount": 0, "seller": "Croma", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Zara F", "rating": 5.0, "title": "Best iPad for students and creators", "body": "The M2 chip makes this iPad feel like a computer. Combined with Magic Keyboard it genuinely replaces my laptop for 80% of tasks. The Liquid Retina display is stunning for digital art with Apple Pencil Pro. Build quality is impeccable. iPadOS 17 multitasking is much improved.", "verified": True, "helpful": 234, "date": "2024-03-28"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [74900, 74900, 74900, 74900, 74900, 74900, 74900, 74900, 74900]},
            {"platform": "Flipkart", "prices_30days": [74900, 74500, 74000, 73500, 73000, 72999, 72999, 72999, 72999]},
        ]
    },
    # ===================== CAMERAS =====================
    {
        "name": "Sony Alpha ZV-E10 II Mirrorless Camera",
        "brand": "Sony",
        "category": "Cameras",
        "subcategory": "Mirrorless Cameras",
        "description": "Compact vlogging mirrorless camera with APS-C sensor, 4K60p video, AI-powered autofocus, and directional 3-capsule microphone.",
        "image_url": "https://images.unsplash.com/photo-1616423640778-28d1b53229bd?w=400",
        "specifications": {
            "Sensor": "26.1MP APS-C Exmor R CMOS",
            "Video": "4K 60fps, 1080p 120fps",
            "Autofocus": "759-point phase-detect AF with AI tracking",
            "Viewfinder": "None (vlog-focused)",
            "Screen": "Vari-angle touchscreen",
            "Connectivity": "WiFi, Bluetooth, USB-C",
            "Battery": "NP-FZ100 (520 shots)",
            "Weight": "293g (body only)",
            "Lens Mount": "Sony E-mount",
            "Special": "3-capsule directional mic, Real-time Eye AF"
        },
        "listings": [
            {"platform": "Amazon", "price": 79990, "original_price": 89990, "discount": 11, "seller": "Sony India", "availability": "in_stock", "delivery": "Free delivery in 2 days"},
            {"platform": "Flipkart", "price": 77999, "original_price": 89990, "discount": 13, "seller": "Flipkart Assured", "availability": "in_stock", "delivery": "Free delivery tomorrow"},
            {"platform": "Croma", "price": 81000, "original_price": 89990, "discount": 10, "seller": "Croma", "availability": "limited_stock", "delivery": "Free delivery in 3 days"},
        ],
        "reviews": [
            {"platform": "Amazon", "name": "Laila T", "rating": 4.5, "title": "Perfect for content creators!", "body": "As a YouTuber this camera is everything I needed. The AI autofocus tracks subjects perfectly even during movement. 4K60p footage is incredible. The directional microphone is surprisingly good for outdoor shots. Vari-angle screen is perfect for self-shooting. Highly recommend for creators on a budget.", "verified": True, "helpful": 312, "date": "2024-03-18"},
        ],
        "price_history_data": [
            {"platform": "Amazon", "prices_30days": [89990, 87000, 85000, 83000, 82000, 81000, 80500, 79990, 79990]},
            {"platform": "Flipkart", "prices_30days": [89990, 86000, 84000, 82000, 81000, 80000, 79000, 78000, 77999]},
        ]
    },
]


def generate_price_history(product_id: int, platform: str, price_series: list, db):
    """Generate daily price history entries for the past 90 days."""
    today = datetime.now()
    num_samples = len(price_series)
    
    for i, price in enumerate(price_series):
        # Add some random variation
        varied_price = price * random.uniform(0.98, 1.02)
        days_ago = int((num_samples - 1 - i) * (90 / num_samples))
        date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        history = PriceHistory(
            product_id=product_id,
            platform=platform,
            price=round(varied_price, 0),
            date=date
        )
        db.add(history)
    
    # Fill remaining days with interpolated values
    last_price = price_series[-1]
    for day in range(5):
        date = (today - timedelta(days=day)).strftime("%Y-%m-%d")
        varied_price = last_price * random.uniform(0.99, 1.01)
        history = PriceHistory(
            product_id=product_id,
            platform=platform,
            price=round(varied_price, 0),
            date=date
        )
        db.add(history)


def seed_database():
    db = SessionLocal()
    
    # Clear existing data
    db.query(PriceHistory).delete()
    db.query(Review).delete()
    db.query(ProductListing).delete()
    db.query(Product).delete()
    db.commit()
    
    print("Seeding database with sample data...")
    
    for product_data in PRODUCTS_DATA:
        # Create product
        product = Product(
            name=product_data["name"],
            brand=product_data["brand"],
            category=product_data["category"],
            subcategory=product_data["subcategory"],
            description=product_data["description"],
            image_url=product_data["image_url"],
            specifications=product_data["specifications"]
        )
        db.add(product)
        db.flush()
        
        # Create listings
        for listing_data in product_data["listings"]:
            listing = ProductListing(
                product_id=product.id,
                platform=listing_data["platform"],
                seller=listing_data["seller"],
                price=listing_data["price"],
                original_price=listing_data["original_price"],
                discount_percent=listing_data["discount"],
                availability=listing_data["availability"],
                delivery_info=listing_data["delivery"],
                in_stock=listing_data["availability"] != "out_of_stock",
                emi_options={
                    "3_months": round(listing_data["price"] / 3),
                    "6_months": round(listing_data["price"] / 6),
                    "12_months": round(listing_data["price"] / 12),
                },
                bank_offers=[
                    "5% cashback on HDFC Credit Cards",
                    "No-cost EMI on SBI Credit Cards",
                    "Instant discount of ₹500 on Kotak Cards"
                ]
            )
            db.add(listing)
        
        # Create reviews
        for review_data in product_data["reviews"]:
            review = Review(
                product_id=product.id,
                platform=review_data["platform"],
                reviewer_name=review_data["name"],
                rating=review_data["rating"],
                title=review_data["title"],
                body=review_data["body"],
                verified_purchase=review_data["verified"],
                helpful_votes=review_data["helpful"],
                review_date=review_data["date"]
            )
            db.add(review)
        
        # Create price history
        for ph_data in product_data.get("price_history_data", []):
            generate_price_history(product.id, ph_data["platform"], ph_data["prices_30days"], db)
        
        print(f"  + Added: {product_data['name']}")
    
    db.commit()
    db.close()
    print(f"\nSeeded {len(PRODUCTS_DATA)} products with listings, reviews, and price history!")


if __name__ == "__main__":
    seed_database()
