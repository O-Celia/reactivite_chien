import streamlit as st
import requests

API_URL = "http://localhost:8000"


def login():
    st.title("Bienvenue !")

    auth_mode = st.radio("Choisir une option :", ["Connexion", "Créer un compte"])

    if auth_mode == "Connexion":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Connexion"):
            response = requests.post(
                f"{API_URL}/users/login",
                timeout=60,
                json={"username": username, "password": password},
            )

            if response.status_code in (200, 201):
                token = response.json()["access_token"]
                st.session_state["token"] = token
                st.session_state["username"] = username
                st.success("Connecté !")
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

    elif auth_mode == "Créer un compte":
        new_username = st.text_input("Nom d'utilisateur", key="signup_user")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Mot de passe", type="password", key="signup_pass")

        if st.button("Créer le compte"):
            if not new_password:
                st.warning("Le mot de passe est obligatoire.")
            else:
                response = requests.post(
                    f"{API_URL}/users/",
                    timeout=60,
                    json={
                        "username": new_username,
                        "email": new_email if new_email else None,
                        "password": new_password,
                    },
                )

                if response.status_code in (201, 200):
                    st.success("Compte créé ! Vous pouvez maintenant vous connecter.")
                elif response.status_code == 400:
                    st.error("Nom d'utilisateur déjà pris.")
                else:
                    st.error(
                        f"Erreur : {response.json().get('detail', 'Erreur inconnue')}"
                    )


def main():
    token = st.session_state.get("token")
    if not token:
        login()
        return

    headers = {"Authorization": f"Bearer {token}"}
    user_info_resp = requests.get(f"{API_URL}/users/me", headers=headers, timeout=60)

    if user_info_resp.status_code != 200:
        st.error("Erreur d’authentification. Veuillez vous reconnecter.")
        st.session_state.clear()
        st.rerun()

    user_info = user_info_resp.json()

    if user_info.get("first_login", False):
        st.subheader("Bienvenue ! Sélectionne tes déclencheurs et réactions")

        try:
            default_triggers = requests.get(
                f"{API_URL}/triggers/default", headers=headers, timeout=60
            ).json()
            default_reactions = requests.get(
                f"{API_URL}/reactions/default", headers=headers, timeout=60
            ).json()
        except:
            st.error(
                "Erreur lors du chargement des déclencheurs ou réactions par défaut."
            )
            return

        trigger_options = {t["name"]: t["id"] for t in default_triggers}
        reaction_options = {r["name"]: r["id"] for r in default_reactions}

        selected_triggers = st.multiselect(
            "Déclencheurs disponibles", trigger_options.keys()
        )
        selected_reactions = st.multiselect(
            "Réactions disponibles", reaction_options.keys()
        )

        if st.button("Valider mes choix"):
            if selected_triggers:
                requests.post(
                    f"{API_URL}/triggers/clone_selected",
                    headers=headers,
                    timeout=60,
                    json={
                        "trigger_ids": [
                            trigger_options[name] for name in selected_triggers
                        ]
                    },
                )
            if selected_reactions:
                requests.post(
                    f"{API_URL}/reactions/clone_selected",
                    headers=headers,
                    timeout=60,
                    json={
                        "reaction_ids": [
                            reaction_options[name] for name in selected_reactions
                        ]
                    },
                )

            requests.patch(
                f"{API_URL}/users/me",
                headers=headers,
                timeout=60,
                json={"first_login": False},
            )
            st.success("C’est enregistré ! Tu peux maintenant utiliser ton espace.")
            st.rerun()
    else:
        show_app()


def show_app():
    import Home
    import dataentry
    import analysis
    import calender
    import research
    import adminentry
    import admin
    import account

    PAGES = {
        "Accueil": Home,
        "Nouvelle observation": dataentry,
        "Calendrier": calender,
        "Recherches": research,
        "Analyses graphiques": analysis,
        "Gestion des observations": adminentry,
        "Administration": admin,
        "Gestion du compte": account,
    }

    st.sidebar.title("Navigation")

    if st.sidebar.button("Se déconnecter"):
        st.session_state.clear()
        st.rerun()

    selection = st.sidebar.selectbox("Aller vers :", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()


# Point d’entrée
if __name__ == "__main__":
    main()
