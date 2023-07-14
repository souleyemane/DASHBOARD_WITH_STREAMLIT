import streamlit as st
st.title("Mon application Streamlit")
st.write("Bienvenue sur mon application !")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fusionner_tables(fichiers):
    if len(fichiers) < 2:
        return {'error': 'Veuillez fournir au moins deux fichiers de données.'}

    tables = []
    for fichier in fichiers:
        if fichier.name.endswith('.csv'):
            tables.append(pd.read_csv(fichier))
        elif fichier.name.endswith('.xlsx'):
            tables.append(pd.read_excel(fichier))
        else:
            return {'error': 'Format de fichier non pris en charge. Veuillez utiliser des fichiers CSV ou Excel.'}

    donnees_fusionnees = tables[0]  # Prend le premier tableau comme point de départ pour la fusion
    for i in range(1, len(tables)):
        donnees_fusionnees = pd.merge(donnees_fusionnees, tables[i], on="cookie_id", how="left")
    return donnees_fusionnees

def main():
    st.title("Dashboard de fusion de données")
    st.write("Veuillez sélectionner au moins deux fichiers de données à fusionner.")

    fichiers = st.file_uploader("Télécharger les fichiers de données", accept_multiple_files=True)
    if fichiers:
        donnees = fusionner_tables(fichiers)
        st.write("Données fusionnées :")
        st.write(donnees)

        # Box plot de l'âge moyen en fonction des product_id
        st.subheader("Box plot de l'âge moyen en fonction des product_id")
        fig = plt.figure(figsize=(10, 6))
        sns.boxplot(x="product_id", y="age", data=donnees)
        plt.xlabel("product_id")
        plt.ylabel("Âge moyen")
        plt.title("Distribution de l'âge moyen en fonction des product_id")
        st.pyplot(fig)

# Diagramme en barres du product_id en fonction de la moyenne des âges
        st.subheader("Product_id en fonction de la moyenne des âges")
        somme_ages_par_produit = donnees.groupby("product_id")["age"].mean()
        fig, ax = plt.subplots(figsize=(10, 6))
        somme_ages_par_produit.plot(kind="bar", ax=ax)
        plt.xlabel("product_id")
        plt.ylabel("moyenne des âges")
        plt.title("moyenne des âges en fonction du product_id")
        st.pyplot(fig)

 # Calcul du chiffre d'affaires
        chiffre_affaires = donnees['price'].sum()

        # Affichage du chiffre d'affaires
        st.subheader("Chiffre d'affaires")
        st.markdown(f"<p style='font-size: 100px; color: red;'>{chiffre_affaires} €</p>", unsafe_allow_html=True)

level = st.slider("Select the level", 1, 5)

st.text('Selected: {}'.format(level))




if __name__ == "__main__":
    main()
