from caddkit.graphs import calculate_mean_std, scale_by_thresholds, plot_radar
import pandas as pd
import pytest
from unittest.mock import patch

def test_calculate_mean_std():
    data = {
        'molecular_weight': [200, 300, 400],
        'n_heavy_atoms': [5, 6, 7],
        'n_rotatable_bonds': [2, 3, 4],
        'n_hbd': [1, 2, 3],
        'n_hba': [4, 5, 6],
        'logp': [1.5, 2.0, 2.5]
    }
    
    df = pd.DataFrame(data)
    result = calculate_mean_std(df)

    assert result.shape == (6, 2)
    assert set(result.columns) == {"mean", "std"}

    expected_means = {
        'molecular_weight': 300,
        'n_heavy_atoms': 6,
        'n_rotatable_bonds': 3,
        'n_hbd': 2,
        'n_hba': 5,
        'logp': 2.0
    }
    expected_stds = {
        'molecular_weight': 100,
        'n_heavy_atoms': 1,
        'n_rotatable_bonds': 1,
        'n_hbd': 1,
        'n_hba': 1,
        'logp': 0.5
    }

    for prop in expected_means:
        assert result.loc[prop, "mean"] == expected_means[prop]
        assert result.loc[prop, "std"] == expected_stds[prop]

def test_scale_by_thresholds():
    stats = pd.DataFrame({
        'mean': [300, 6, 3, 2, 5, 2.0],
        'std': [100, 1, 1, 1, 1, 0.5]
    }, index=['molecular_weight', 'n_heavy_atoms', 'n_rotatable_bonds', 'n_hbd', 'n_hba', 'logp'])

    thresholds = {
        'molecular_weight': 500,
        'n_heavy_atoms': 10,
        'n_rotatable_bonds': 12,
        'n_hbd': 5,
        'n_hba': 10,
        'logp': 5
    }

    scaled_threshold = 5
    result = scale_by_thresholds(stats, thresholds, scaled_threshold)

    expected_scaled = {
        'molecular_weight': 300 * 5 / 500,
        'n_heavy_atoms': 6 * 5 / 10,
        'n_rotatable_bonds': 3 * 5 / 12,
        'n_hbd': 2 * 5 / 5,
        'n_hba': 5 * 5 / 10,
        'logp': 2.0 * 5 / 5
    }

    for prop in expected_scaled:
        assert result.loc[prop, "mean"] == pytest.approx(expected_scaled[prop], rel=1e-2)

def test_plot_radar():
    data = {
        'molecular_weight': [200, 300, 400],
        'n_heavy_atoms': [5, 6, 7],
        'n_rotatable_bonds': [2, 3, 4],
        'n_hbd': [1, 2, 3],
        'n_hba': [4, 5, 6],
        'logp': [1.5, 2.0, 2.5]
    }

    df = pd.DataFrame(data)
    stats = calculate_mean_std(df)

    thresholds = {
        'molecular_weight': 500,
        'n_heavy_atoms': 10,
        'n_rotatable_bonds': 12,
        'n_hbd': 5,
        'n_hba': 10,
        'logp': 5
    }

    scaled_threshold = 5
    properties_labels = [
        "Molecular weight (Da) / 100",
        "# HBA / 2",
        "# HBD",
        "LogP"
    ]
    y_max = 8

    with patch("matplotlib.pyplot.show") as mock_show:
        plot_radar(stats, thresholds, scaled_threshold, properties_labels, y_max)
        mock_show.assert_called_once()

if __name__ == "__main__":
    pytest.main()