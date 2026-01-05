"""
Data transformation utilities.
Functions for DataFrame manipulation, filtering, and translation.
"""
import pandas as pd
import prompts


def df_filter_by(df: pd.DataFrame, query_string: str) -> pd.DataFrame:
    """Filters a DataFrame using a query string.
    
    Args:
        df: The DataFrame to filter.
        query_string: The query expression to apply.
    
    Returns:
        The filtered DataFrame.
    """
    try:
        return df.query(query_string)
    except Exception as e:
        print(f"Error during query '{query_string}': {e}")
        return df


def translate_to_english(df: pd.DataFrame) -> pd.DataFrame:
    """Translates a Brazilian Portuguese DataFrame to English.
    
    Handles category index translation and column renaming.
    Uses the mapper from prompts module.
    
    Args:
        df: DataFrame with Portuguese column names and values.
    
    Returns:
        Translated DataFrame with English column names and values.
    """
    df_final = (
        df
        .rename(index={
            "Eletrônicos": "Electronics", 
            "Móveis": "Furniture", 
            "Roupas": "Clothing", 
            "Eletrodomésticos": "Appliances"
        })
        .reset_index()
        .rename(columns={
            "Categoria do Produto": "Category",
            "Nome do Produto": "Name",
            "Preço do produto": "Price",
            "Quantidade do produto que foram vendidas": "Quantity",
            "Avaliação do Produto": "Rating"
        })
    )

    mask = df_final["Name"].isin(prompts.mapper.keys())
    df_final.loc[mask, "Name"] = df_final.loc[mask, "Name"].map(prompts.mapper)
    return df_final
