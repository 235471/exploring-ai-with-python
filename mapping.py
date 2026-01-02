mapper = {
    "Notebook Pro 15": "Notebook Pro 15",
    "Smartphone X": "Smartphone X",
    "Fone Bluetooth": "Bluetooth Headphones",
    "Smart TV 50\"": "50\" Smart TV",
    "Mouse Gamer": "Gaming Mouse",
    "Teclado Mecânico": "Mechanical Keyboard",
    "Monitor 27\"": "27\" Monitor",
    "Câmera Digital": "Digital Camera",
    "Tablet Plus": "Tablet Plus",
    "Carregador USB": "USB Charger",
    "Cadeira Gamer": "Gaming Chair",
    "Mesa Escritório": "Office Desk",
    "Sofá 3 Lugares": "3-Seater Sofa",
    "Estante de Livros": "Bookshelf",
    "Guarda-Roupa": "Wardrobe",
    "Cama Box": "Box Bed",
    "Poltrona": "Armchair",
    "Rack TV": "TV Stand",
    "Mesa Jantar": "Dining Table",
    "Banco Alto": "Bar Stool",
    "Camiseta Básica": "Basic T-Shirt",
    "Calça Jeans": "Jeans",
    "Jaqueta": "Jacket",
    "Vestido Casual": "Casual Dress",
    "Tênis Esportivo": "Sports Sneakers",
    "Moletom": "Sweatshirt",
    "Shorts": "Shorts",
    "Saia": "Skirt",
    "Camisa Social": "Dress Shirt",
    "Meias": "Socks",
    "Liquidificador": "Blender",
    "Air Fryer": "Air Fryer",
    "Cafeteira": "Coffee Maker",
    "Micro-ondas": "Microwave",
    "Geladeira": "Refrigerator",
    "Fogão": "Stove",
    "Aspirador Pó": "Vacuum Cleaner",
    "Ventilador": "Fan",
    "Batedeira": "Stand Mixer",
    "Sanduicheira": "Sandwich Maker"
}

# AI Prompt configurations for review analysis
# Each config contains: prompt template, regex pattern, and output column name
AI_PROMPTS = {
    "feelings": {
        "prompt": """You are a professional sentiment analyzer.
        I will provide {count} customer reviews. 
        Your task is to classify each one as: positive, neutral, or negative.
        Rules:
        1. Return ONLY a numbered list of labels.
        2. Do not include the original review or any introductory text.
        3. Match the labels to the review numbers exactly.
        Input Reviews:
        {reviews}
        Example Output:
        1. positive
        2. negative
        3. neutral
        ... and so on.
        Output:""",
        "regex": r"\d+\.\s*(positive|neutral|negative)",
        "column": "feeling"
    },
    "categories": {
        "prompt": """You are a professional sentiment analyzer.
        I will provide {count} negative customer reviews. 
        You have to create general categories for those reviews when they differ.
        Rules:
        1. Return ONLY a numbered list of categories.
        2. Do not include the original review or any introductory text.
        3. Match the categories to the review numbers exactly.
        Input Reviews:
        {reviews}
        Example Output:
        1. category
        2. category
        ... and so on.
        Output:""",
        "regex": r"\d+\.\s*(.+)",
        "column": "category"
    }
}
