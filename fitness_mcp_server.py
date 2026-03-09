from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("fitness-tools")


@mcp.tool()
@mcp.tool()
def get_nutrition(food: str) -> str:
    print("---- TOOL CALLED ----")
    print("Food:", food)

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": food,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    headers = {
        "User-Agent": "FitnessAIApp/1.0"
    }

    session = requests.Session()
    session.headers.update({
        "User-Agent": "FitnessAIApp/1.0"
    })

    try:
        response = session.get(
            url,
            params=params,
            headers=headers,
            timeout=(5,30)   # 5 sec connect, 30 sec read
        )

        print("Status Code:", response.status_code)
        print("Raw Response (first 500 chars):")
        print(response.text[:500])

        response.raise_for_status()

    except Exception as e:
        print("API ERROR:", str(e))
        return f"API request failed: {str(e)}"

    data = response.json()

    print("Products found:", len(data.get("products", [])))

    if not data.get("products"):
        return "No nutrition data found."

    product = data["products"][0]
    nutriments = product.get("nutriments", {})

    calories = nutriments.get("energy-kcal_100g", "N/A")
    protein = nutriments.get("proteins_100g", "N/A")
    carbs = nutriments.get("carbohydrates_100g", "N/A")
    fat = nutriments.get("fat_100g", "N/A")

    name = product.get("product_name", food)

    return (
        f"{name} (per 100g):\n"
        f"Calories: {calories} kcal\n"
        f"Protein: {protein} g\n"
        f"Carbs: {carbs} g\n"
        f"Fat: {fat} g"
    )

if __name__ == "__main__":
    print("🚀 Starting MCP server...")
    mcp.run(transport="sse")