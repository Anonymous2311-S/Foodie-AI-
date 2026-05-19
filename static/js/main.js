document.addEventListener('DOMContentLoaded', () => {
    const calorieSlider = document.getElementById('max_calories');
    const calorieValue = document.getElementById('calorie-value');
    const filterForm = document.getElementById('filter-form');
    const resultsSection = document.getElementById('results-section');

    // Update calorie value display on slide
    calorieSlider.addEventListener('input', (e) => {
        calorieValue.textContent = e.target.value;
    });

    // Handle form submission
    filterForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form data
        const formData = new FormData(filterForm);
        const data = {
            cuisine: formData.get('cuisine'),
            vegetarian: formData.get('vegetarian') === 'on',
            vegan: formData.get('vegan') === 'on',
            gluten_free: formData.get('gluten_free') === 'on',
            max_calories: formData.get('max_calories')
        };

        // Show loading state (could add a spinner here)
        resultsSection.innerHTML = `
            <div class="placeholder-state glass-panel" style="animation: pulse 1.5s infinite">
                <p>Curating your culinary experience...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const recipes = await response.json();
            renderRecipes(recipes);

        } catch (error) {
            console.error('Error fetching recommendations:', error);
            resultsSection.innerHTML = `
                <div class="placeholder-state glass-panel" style="border-color: #ff3366;">
                    <p>Oops! Something went wrong while fetching recipes. Please try again.</p>
                </div>
            `;
        }
    });

    function renderRecipes(recipes) {
        if (recipes.length === 0) {
            resultsSection.innerHTML = `
                <div class="placeholder-state glass-panel">
                    <p>No recipes found matching your exact criteria. Try loosening your restrictions!</p>
                </div>
            `;
            return;
        }

        resultsSection.innerHTML = '';
        
        recipes.forEach((recipe, index) => {
            // Calculate a staggered animation delay based on index
            const animationDelay = `${index * 0.1}s`;
            
            const card = document.createElement('div');
            card.className = 'recipe-card';
            card.style.animation = `scaleIn 0.5s ease-out ${animationDelay} both`;
            
            // Build badges HTML
            let badgesHtml = '';
            if (recipe.is_vegan) badgesHtml += '<span class="badge vegan">Vegan</span>';
            else if (recipe.is_vegetarian) badgesHtml += '<span class="badge veg">Veg</span>';
            if (recipe.is_gluten_free) badgesHtml += '<span class="badge gf">GF</span>';

            card.innerHTML = `
                <div class="recipe-image" style="background-image: url('${recipe.image_url}')">
                    <div class="recipe-badges">
                        ${badgesHtml}
                    </div>
                </div>
                <div class="recipe-content">
                    <h3>${recipe.recipe_name}</h3>
                    <div class="recipe-meta">
                        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px; margin-top: -2px;"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> ${recipe.cuisine}</span>
                    </div>
                    <div class="recipe-ingredients">
                        <strong>Ingredients:</strong> ${recipe.ingredients}
                    </div>
                    <div class="recipe-footer">
                        <span class="calories">${recipe.calories} kcal</span>
                        <button class="btn-secondary" onclick="alert('Recipe details coming soon!')" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 6px 12px; border-radius: 8px; cursor: pointer; transition: all 0.2s;">
                            View Details
                        </button>
                    </div>
                </div>
            `;
            resultsSection.appendChild(card);
        });
    }
});

// Add pulse animation dynamically
const style = document.createElement('style');
style.innerHTML = `
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}
`;
document.head.appendChild(style);
