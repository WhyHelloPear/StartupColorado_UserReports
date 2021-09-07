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
            "Internet of Things (IOT)",
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
        if(content == "Marketing Promotions"):
            return "Marketing & Promotions"
        elif(content == "Coaching Mentorship"):
            return "Coaching & Mentorship"
        elif(content == 'Outoor Recreation'):
            return 'Outdoor Recreation'
        else:
            return content

        