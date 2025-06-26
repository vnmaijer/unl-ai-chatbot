
# UNL AI Chatbot (Flask)

## Instructies

1. Voeg de volgende environment variables toe aan je Azure Web App:
   - `CLIENT_ID` = jouw Azure AD App Client ID
   - `CLIENT_SECRET` = jouw geheime sleutel
   - `TENANT_ID` = c38a20c7-169c-434f-b89f-45025169197e
   - `OPENAI_API_KEY` = jouw OpenAI API sleutel

2. Deploy de app naar Azure via GitHub of zip-upload.

3. Zorg dat je app in Azure AD is geregistreerd met redirect URI:
   `https://unl-ai-chatbot.azurewebsites.net/login`

4. Alleen gebruikers met e-mails eindigend op `@unl.nl` hebben toegang.
# unl-ai-chatbot
