from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Initialize OpenAI client
client = Groq(
    api_key ="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",
)


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecipeRequest(BaseModel):
    recipe_name: str
    language_option: str

def get_recipe(recipe_name, language_option):
    if language_option == "தமிழ்":
        prompt_template = f"""
        நீங்கள் ஒரு தொழில்முறை சமையல்காரர் மற்றும் சமையல் உதவியாளர். உங்கள் பணி, தெளிவான வழிமுறைகள், வகைப்படுத்தப்பட்ட படிகள் மற்றும் மதிப்பிடப்பட்ட கால அளவுகளுடன் ஒரு கட்டமைக்கப்பட்ட, படிப்படியான செய்முறை வழிகாட்டியை வழங்குவதாகும்.

        செய்முறை பெயர்: {recipe_name}

        உள்ளீட்டு பணி: ஒரு கப் தேநீர் தயாரிக்கவும்
        வெளியீடு: வழிமுறைகளின் வரிசை:
        
        1. வழிமுறை 1: ஒரு தேநீர் பையையும் ஒரு கப்பையும் எடுத்துக் கொள்ளுங்கள்.
           • வகை: எளிய வழிமுறை
           காலம்: 30 வினாடிகள்
        2. வழிமுறை 2: தேநீர் தயாரிக்கும் நோக்கத்துடன் தண்ணீரை கொதிக்க வைக்கவும்.
           • வகை: நோக்கம் கொண்ட வழிமுறை
           காலம்: 2 நிமிடங்கள்
        3. வழிமுறை 3: கொதிக்கும் தண்ணீரை தேநீர் பையுடன் கப்பில் ஊற்றவும்.
           • வகை: வரிசை கொண்ட வழிமுறை
           காலம்: 30 வினாடிகள்
        4. வழிமுறை 4: விருப்பமாக, தேநீரில் சர்க்கரை அல்லது பால் சேர்க்கவும்.
           • வகை: விருப்ப வழிமுறை
           காலம்: 1 நிமிடம் (விருப்பமானது)
        5. வழிமுறை 5: பின்னர், தேநீரை பரிமாறவும்.
           • வகை: வரிசை கொண்ட வழிமுறை
           காலம்: 30 வினாடிகள்
        மொத்த நேர கணக்கீடு:
           • சர்க்கரை அல்லது பால் சேர்த்தல் இல்லாமல்: 3 நிமிடங்கள் 30 வினாடிகள்
           • சர்க்கரை அல்லது பால் சேர்த்தால்: 4 நிமிடங்கள் 30 வினாடிகள்

        இப்போது, *{recipe_name}*க்கான படிப்படியான வழிமுறைகளை மேலே உள்ள கட்டமைப்பைப் பின்பற்றி உருவாக்கவும்.
        """
    elif language_option == "Français":
        prompt_template = f"""
        Vous êtes un chef professionnel et assistant culinaire. Votre tâche consiste à fournir un guide de recette structuré, étape par étape, avec des instructions claires, des étapes catégorisées et des durées estimées.

        Nom de la recette: {recipe_name}

        Tâche D'ENTRÉE: Préparer une tasse de thé
        RÉSULTAT: Séquence d'instructions:
        
        1. Instruction 1: Prenez un sachet de thé et une tasse.
           • Type: INSTRUCTION SIMPLE
           Durée: 30 secondes
        2. Instruction 2: Faites bouillir de l'eau avec l'intention de faire du thé.
           • Type: INSTRUCTION AVEC OBJECTIF
           Durée: 2 minutes
        3. Instruction 3: Versez l'eau bouillie dans la tasse avec le sachet de thé.
           • Type: INSTRUCTION AVEC SÉQUENCE
           Durée: 30 secondes
        4. Instruction 4: Optionnellement, ajoutez du sucre ou du lait au thé.
           • Type: INSTRUCTION EXCLUSIVE
           Durée: 1 minute (facultatif)
        5. Instruction 5: Ensuite, servez le thé.
           • Type: INSTRUCTION AVEC SÉQUENCE
           Durée: 30 secondes
        Calcul du temps total:
           • Sans ajouter de sucre ou de lait: 3 minutes 30 secondes
           • Avec ajout de sucre ou de lait: 4 minutes 30 secondes

        Maintenant, générez les instructions étape par étape pour {recipe_name} en suivant le format structuré ci-dessus.
        """
    elif language_option == "മലയാളം":
        prompt_template = f"""
        നിങ്ങൾ ഒരു പ്രൊഫഷണൽ ഷെഫ് ആയും പാചക സഹായിയുമായാണ് പ്രവർത്തിക്കുന്നത്. നിങ്ങളുടെ ദൗത്യമാണ്, വ്യക്തമായ നിർദ്ദേശങ്ങൾ, വിഭാഗീകരിച്ച ഘട്ടങ്ങൾ, സമയക്രമീകരണങ്ങൾ എന്നിവയോടെയുള്ള ഒരു ക്രമീകരിച്ച പാചക മാർഗരേഖ നൽകുക.

        റെസിപ്പി പേര്: {recipe_name}

        ഇൻപുട്ട് ദൗത്യം: ഒരു കപ്പ് ചായ ഒരുക്കുക
        ഔട്ട്പുട്ട്: ഘട്ടങ്ങളിലെ നിർദ്ദേശങ്ങളുടെ ക്രമം:
        
        1. ഘട്ടം 1: ഒരു ടീ ബാഗും ഒരു കപ്പും എടുക്കുക.
           • തരം: ലളിത നിർദ്ദേശം
           ദൈർഘ്യം: 30 സെക്കൻഡ്
        2. ഘട്ടം 2: ചായ ഉണ്ടാക്കാൻ ഉദ്ദേശത്തോടെ വെള്ളം കുതിരിക്കുക.
           • തരം: ലക്ഷ്യ സഹിതം നിർദ്ദേശം
           ദൈർഘ്യം: 2 മിനിറ്റ്
        3. ഘട്ടം 3: ചൂടാക്കിയ വെള്ളം, ടി ബാഗുള്ള കപ്പിലേക്ക് ഒഴിക്കുക.
           • തരം: ക്രമ നിർദ്ദേശം
           ദൈർഘ്യം: 30 സെക്കൻഡ്
        4. ഘട്ടം 4: ഐച്ഛികമായി, ചായയിൽ പഞ്ചസാരയോ പാലിനോ ചേർക്കുക.
           • തരം: ഐച്ഛിക നിർദ്ദേശം
           ദൈർഘ്യം: 1 മിനിറ്റ്
        5. ഘട്ടം 5: ശേഷം, ചായ പരിവഹിക്കുക.
           • തരം: ക്രമ നിർദ്ദേശം
           ദൈർഘ്യം: 30 സെക്കൻഡ്
        മൊത്തം സമയം:
           • പഞ്ചസാര/പാലില്ലാതെ: 3 മിനിറ്റ് 30 സെക്കൻഡ്
           • പഞ്ചസാര/പാലോടുകൂടി: 4 മിനിറ്റ് 30 സെക്കൻഡ്

        ഇനി, {recipe_name} എന്നതിനുത്തരം ക്രമീകരിച്ച പാചക മാർഗരേഖ തയ്യാറാക്കുക.
        """
    elif language_option == "తెలుగు":
        prompt_template = f"""
        మీరు ఒక ప్రొఫెషనల్ చెఫ్ మరియు వంట సహాయకుడిగా వ్యవహరిస్తున్నారు. మీ పని, స్పష్టమైన సూచనలతో, విభాగాలుగా వర్గీకరించిన దశలతో మరియు గణించబడిన సమయాలతో సహా ఒక సుసంపన్నమైన వంటకాల గైడ్‌ని అందించడం.

        వంటకపు పేరు: {recipe_name}

        ఇన్పుట్ టాస్క్: ఒక కప్పు టీ ను తయారుచేయండి
        ఔట్‌పుట్: దశలవారీ సూచనల శ్రేణి:
        
        1. దశ 1: ఒక టీ బ్యాగ్ మరియు ఒక కప్పును తీసుకోండి.
           • తరగతి: సులభమైన సూచన
           వ్యవధి: 30 సెకన్లు
        2. దశ 2: టీ తయారుచేయడానికి నీటిని మరిగించండి.
           • తరగతి: ఉద్దేశ్యంతో కూడిన సూచన
           వ్యవధి: 2 నిమిషాలు
        3. దశ 3: మరిగిన నీటిని టీ బ్యాగ్ ఉన్న కప్పులో పోయండి.
           • తరగతి: అనుక్రమ సూచన
           వ్యవధి: 30 సెకన్లు
        4. దశ 4: ఐచ్చికంగా, చక్కెర లేదా పాలను జోడించండి.
           • తరగతి: ఐచ్చిక సూచన
           వ్యవధి: 1 నిమిషం
        5. దశ 5: తరువాత, టీని సర్వ్ చేయండి.
           • తరగతి: అనుక్రమ సూచన
           వ్యవధి: 30 సెకన్లు
        మొత్తం సమయం:
           • చక్కెర/పాలు లేకుండా: 3 నిమిషాలు 30 సెకన్లు
           • చక్కెర/పాలు ఉంటే: 4 నిమిషాలు 30 సెకన్లు

        ఇప్పుడు, {recipe_name} కోసం పై నిర్మిత నమూనా ప్రకారం దశలవారీ సూచనలను రూపొందించండి.
        """
    elif language_option == "ಕನ್ನಡ":
        prompt_template = f"""
        ನೀವೊಂದು ಪ್ರೊಫೆಷನಲ್ ಶೆಫ್ ಮತ್ತು ಅಡುಗೆ ಸಹಾಯಕರಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತೀರಿ. ನಿಮ್ಮ ಕರ್ತವ್ಯವೆಂದರೆ, ಸ್ಪಷ್ಟ ಸೂಚನೆಗಳು, ವಿಭಾಗೀಕರಿಸಿದ ಹಂತಗಳು ಮತ್ತು ಅಂದಾಜು ಕಾಲಾವಧಿಗಳೊಂದಿಗೆ ಪರಿಚಯಿತವಾದ ಪಾಕವಿಧಾನ ಮಾರ್ಗದರ್ಶನವನ್ನು ಒದಗಿಸುವುದು.

        ರೆಸಿಪಿಯ ಹೆಸರು: {recipe_name}

        ಇನ್ಪುಟ್ ಕೆಲಸ: ಒಂದು ಕಪ್ ಚಹಾ ತಯಾರಿಸಿ
        ಔಟ್‌ಪುಟ್: ಹಂತ ಹಂತದ ಸೂಚನೆಗಳು:
        
        1. ಹಂತ 1: ಒಂದು ಟೀಸ್ ಬ್ಯಾಗ್ ಮತ್ತು ಒಂದು ಕಪ್ ಅನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ.
           • ಪ್ರಕಾರ: ಸರಳ ಸೂಚನೆ
           ಅವಧಿ: 30 ಸೆಕೆಂಡು
        2. ಹಂತ 2: ಚಹಾ ಮಾಡಲು ನೀರನ್ನು ಕುದಿಸಿ.
           • ಪ್ರಕಾರ: ಉದ್ದೇಶ ಸೂಚನೆ
           ಅವಧಿ: 2 ನಿಮಿಷ
        3. ಹಂತ 3: ಕುದಿದ ನೀರನ್ನು ಟೀಸ್ ಬ್ಯಾಗ್ ಇರುವ ಕಪ್‌ಗೆ ಹಾಕಿ.
           • ಪ್ರಕಾರ: ಕ್ರಮ ಸೂಚನೆ
           ಅವಧಿ: 30 ಸೆಕೆಂಡು
        4. ಹಂತ 4: ಆಯ್ಕೆಯಂತೆ, ಚಹೆಗೆ ಸಕ್ಕರೆ ಅಥವಾ ಹಾಲು ಸೇರಿಸಿ.
           • ಪ್ರಕಾರ: ಐಚ್ಛಿಕ ಸೂಚನೆ
           ಅವಧಿ: 1 ನಿಮಿಷ
        5. ಹಂತ 5: ನಂತರ, ಚಹಾವನ್ನು ಸರ್ವ್ ಮಾಡಿ.
           • ಪ್ರಕಾರ: ಕ್ರಮ ಸೂಚನೆ
           ಅವಧಿ: 30 ಸೆಕೆಂಡು
        ಒಟ್ಟು ಸಮಯ ಲೆಕ್ಕ:
           • ಸಕ್ಕರೆ/ಹಾಲಿಲ್ಲದೆ: 3 ನಿಮಿಷ 30 ಸೆಕೆಂಡು
           • ಸಕ್ಕರೆ/ಹಾಲು ಸೇರಿಸಿದರೆ: 4 ನಿಮಿಷ 30 ಸೆಕೆಂಡು

        ಈಗ, {recipe_name} ಗೆ ಸಂಬಂಧಿಸಿದ ಹಂತ ಹಂತದ ಪಾಕವಿಧಾನ ಸೂಚನೆಗಳನ್ನು ರಚಿಸಿ.
        """
    elif language_option == "हिन्दी":
        prompt_template = f"""
        आप एक पेशेवर शेफ और कुकिंग असिस्टेंट हैं। आपका कार्य स्पष्ट निर्देशों, क्रमबद्ध चरणों और अनुमानित समय के साथ एक संरचित रेसिपी गाइड प्रदान करना है।

        रेसिपी का नाम: {recipe_name}

        इनपुट कार्य: एक कप चाय तैयार करें
        आउटपुट: चरण-दर-चरण निर्देश:
        
        1. चरण 1: एक टी बैग और एक कप लें।
           • प्रकार: साधारण निर्देश
           अवधि: 30 सेकंड
        2. चरण 2: चाय बनाने के लिए पानी को उबालें।
           • प्रकार: उद्देश्य निर्देश
           अवधि: 2 मिनट
        3. चरण 3: उबले हुए पानी को टी बैग वाले कप में डालें।
           • प्रकार: क्रम निर्देश
           अवधि: 30 सेकंड
        4. चरण 4: वैकल्पिक रूप से, चाय में चीनी या दूध मिलाएं।
           • प्रकार: वैकल्पिक निर्देश
           अवधि: 1 मिनट
        5. चरण 5: फिर, चाय परोसें।
           • प्रकार: क्रम निर्देश
           अवधि: 30 सेकंड
        कुल समय:
           • बिना चीनी/दूध के: 3 मिनट 30 सेकंड
           • चीनी/दूध के साथ: 4 मिनट 30 सेकंड

        अब, {recipe_name} के लिए ऊपर दिए गए संरचित प्रारूप का पालन करते हुए चरण-दर-चरण निर्देश तैयार करें।
        """
    else:
        prompt_template = f"""
        You are a professional chef and cooking assistant. Your task is to provide a structured, step-by-step recipe guide with clear instructions, categorized steps, and estimated durations.

        Recipe Name: {recipe_name}

        INPUT Task: Prepare a Cup of Tea
        OUTPUT: Sequence of Instructions:
        
        1. Instruction 1: Take a tea bag and a cup.
           • Type: SIMPLE INSTRUCTION
           Duration: 30 seconds
        2. Instruction 2: Boil water with the intention of making tea.
           • Type: INSTRUCTION WITH PURPOSE
           Duration: 2 minutes
        3. Instruction 3: Pour the boiled water into the cup with the tea bag.
           • Type: INSTRUCTION WITH SEQUENCE
           Duration: 30 seconds
        4. Instruction 4: Optionally, add sugar or milk to the tea.
           Type: EXCLUSIVE INSTRUCTION
           Duration: 1 minute (optional)
        5. Instruction 5: Then, serve the tea.
           • Type: INSTRUCTION WITH SEQUENCE
           Duration: 30 seconds
        Total Time Calculation:
           • Without adding sugar or milk: 3 minutes 30 seconds
           • With adding sugar or milk: 4 minutes 30 seconds

        Now, generate the step-by-step instructions for {recipe_name} following the above structured format.
        """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional chef and cooking assistant."},
            {"role": "user", "content": prompt_template}
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


@app.post("/generate-recipe")
async def generate_recipe(request: RecipeRequest):
    try:
        recipe = get_recipe(request.recipe_name, request.language_option)
        return {"recipe": recipe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)