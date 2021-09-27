class DesiredContent:
    def __init__(self):
        # self.industries = []
        # self.interests = []
        # self.expertise = []

        self.industries = [
            "Accelerator",
            "Aerospace",
            "Agriculture",
            "Arts & Entertainment",
            "Biotechnology",
            "Cannabis",
            "Construction & Engineering",
            "Consumer Goods",
            "Coworking Space",
            "Ecosystem Builder & Small Business Support",
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
            "Hospitality & Tourism",
            "Human Resources",
            "Incubator",
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
            "Getting a job",
            "Customer Service"
        ]
    
    def MapContent(self, content):
        if( ("Marketing" in content) or (content == "Content") ):
            return "Marketing & Content"
        elif("Mentorship" in content):
            return "Coaching & Mentorship"
        elif( content == "Promotions" ):
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
        elif(content == "Recruitment/Hiring"):
            return "Hiring"
        elif("Human Resources" in content):
            return "Human Resources"
        elif(content == "Coworking space"):
            return "Coworking space"
        elif( (content == "Ecosystem Builder") or (content == "Small Business Support") ):
            return "Ecosystem Builder & Small Business Support"
        elif(content == "Environmental & Natural Resources"):
            return "Environmental Resources"

        elif(content == "Environmental & Natural Resources"):
            return "Environmental Resources"
        elif(content == "Environmental & Natural Resources"):
            return "Environmental Resources"
        elif(content == "Environmental & Natural Resources"):
            return "Environmental Resources"
        else:
            return content

        