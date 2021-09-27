class DesiredContent:
    def __init__(self):
        self.industries = [
            "Accelerator & Incubator",
            "Aerospace",
            "Agriculture",
            "Arts and Entertainment",
            "Biotechnology",
            "Cannabis",
            "Construction & Engineering",
            "Consumer Goods",
            "Coworking Space",
            "Ecosystem Builder & Small Business",
            "Education",
            "Energy",
            "Environmental Resources",
            "Finance",
            "Fitness & Wellness",
            "Food & Beverage",
            "Funding",
            "Government & Policy",
            "Hardware Technology",
            "Healthcare",
            "Hospitality",
            "Human Resources",
            "Insurance",
            "Internet of Things (IoT)",
            "Legal",
            "Manufacturing",
            "Marketing & Advertising",
            "Media",
            "Mining & Reclamation",
            "Nonprofit & Philanthropic",
            "Outdoor Recreation",
            "Real Estate",
            "Software Technology",
            "Transportation & Logistics",
            "Sustainability"
        ]

        self.expertise = [
            "Coaching & Mentorship",
            "Marketing & Content",
            "Sales & Promotions",
            "Product Development",
            "Leadership & Management",
            "Human Resources",
            "Financial",
            "Legal",
            "Business Planning",
            "Hiring",
            "Customer Service"
        ]

        self.interests = [
            "Coaching & Mentorship",
            "Marketing & Content",
            "Sales & Promotions",
            "Product Development",
            "Leadership & Management",
            "Human Resources",
            "Financial",
            "Legal",
            "Business Planning",
            "Hiring",
            "Customer Service"
        ]
    
    def MapContent(self, content):
        if( "Advertising" in content ):
            return "Marketing & Advertising"
        elif( "Marketing" in content or "Content" in content or "Product/Market" in content):
            return "Marketing & Content"
        
        elif("Mentorship" in content or content == "Access or referrals to professional services"
                or content == "Education & training"):
            return "Coaching & Mentorship"
        elif( "Promotions" in content or content == "Industry Connections / Networking" or content == "Community Outreach"
                or content == "Community Connections" ):
            return "Sales & Promotions"
        elif(content == "Outoor Recreation"):
            return "Outdoor Recreation"
        elif( (content == "Development") or ("Product Development" in content) ):
            return "Product Development"
        elif( "Management" in content):
            return "Leadership & Management"
        elif(content == "Financial Funding"):
            return "Financial & Funding"
        elif( ("Launching a Business" in content) or (content == "Strategic Planning") or
                    (content == "Planning") or (content == "Business Health Wellness") or (content == "Business") ):
            return "Business Planning"
        elif(content == "Recruitment" in content or "Hiring" in content or "job" in content):
            return "Hiring"
        elif( "Ecosystem Builder" in content or "Small Business" in content ):
            return "Ecosystem Builder & Small Business"
        elif(content == "Environmental & Natural Resources"):
            return "Environmental Resources"
        elif("Accelerator" in content or "Incubator" in content):
            return "Accelerator & Incubator"
        elif("Arts" in content or "Entertainment" in content):
            return "Arts and Entertainment"
        elif("Hospitality" in content or "Tourism" in content):
            return "Hospitality"
        elif("Mining" in content or "Reclamation" in content):
            return "Mining & Reclamation"
        elif("Coworking" in content):
            return "Coworking Space"
        elif("Human" in content and "Resources" in content):
            return "Human Resources"
        elif("Sustainability" in content):
            return "Sustainability"
        elif("Hemp" in content or "Marijuana" in content):
            return "Cannabis"
        elif("Music" in content or content == "Graphic Design"):
            return "Media"
        elif(content == "Professional Services"):
            return "Human Resources"
        elif("Planning" in content or "Growth" in content or "Scaling" in content or "Strategies" in content
                or content == "Business Model Canvas" or "Plan" in content or content == "Customer Acquisition"):
            return "Business Planning"
        elif(content == "Fundraising"):
            return "Financial"
        elif(content == "Pitch Coach" or content == "Troubleshooting Support"):
            return "Customer Service"
        elif("Recruitment" in content):
            return "Hiring"
        elif( content == "Grant Writing" ):
            return "Legal"
        elif( "IT" in content):
            return "Internet of Things (IoT)"
        else:
            return content