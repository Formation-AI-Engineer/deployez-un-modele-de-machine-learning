"""Unit tests — preprocessing pipeline (single-row inference path)."""

from app.preprocessing import EXPECTED_FEATURES, preprocess_single


def test_preprocess_single_produces_expected_columns(sample_input):
    X = preprocess_single(sample_input)
    assert list(X.columns) == EXPECTED_FEATURES
    assert X.shape == (1, len(EXPECTED_FEATURES))


def test_preprocess_single_binary_encoding(sample_input):
    sample_input["genre"] = "F"
    sample_input["heure_supplementaires"] = "Oui"
    X = preprocess_single(sample_input)
    assert X.loc[0, "genre"] == 0
    assert X.loc[0, "heure_supplementaires"] == 1


def test_preprocess_single_ordinal_encoding(sample_input):
    sample_input["frequence_deplacement"] = "Frequent"
    X = preprocess_single(sample_input)
    assert X.loc[0, "frequence_deplacement"] == 2


def test_preprocess_single_engineered_features(sample_input):
    X = preprocess_single(sample_input)
    expected_ratio = (
        sample_input["annees_dans_l_entreprise"] / sample_input["annee_experience_totale"]
    )
    assert X.loc[0, "ratio_anciennete_experience"] == expected_ratio
    assert X.loc[0, "satisfaction_moyenne"] > 0
    assert (
        X.loc[0, "ecart_evaluation"]
        == sample_input["note_evaluation_actuelle"] - sample_input["note_evaluation_precedente"]
    )


def test_preprocess_single_one_hot_encoding(sample_input):
    sample_input["poste"] = "Manager"
    sample_input["departement"] = "Consulting"
    X = preprocess_single(sample_input)
    assert X.loc[0, "poste_Manager"] == 1
    assert X.loc[0, "poste_Consultant"] == 0
    assert X.loc[0, "departement_Consulting"] == 1


def test_preprocess_single_handles_zero_experience(sample_input):
    sample_input["annee_experience_totale"] = 0
    sample_input["annees_dans_l_entreprise"] = 0
    X = preprocess_single(sample_input)
    assert X.loc[0, "ratio_anciennete_experience"] == 0
