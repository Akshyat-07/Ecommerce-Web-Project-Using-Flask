const productGrid = document.getElementById("productGrid");
const statusText = document.getElementById("status");
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const modal = document.getElementById("modal");

const currency = value => new Intl.NumberFormat("en-IN", {
  style: "currency", currency: "INR", maximumFractionDigits: 2
}).format(value);

function safeImage(url) {
  return url || "https://placehold.co/600x400?text=Product";
}

async function loadProducts() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.set("search", searchInput.value.trim());
  if (categoryFilter.value) params.set("category", categoryFilter.value);

  statusText.textContent = "Loading products...";
  try {
    const response = await fetch(`/api/products?${params.toString()}`);
    if (!response.ok) throw new Error("Unable to load products.");
    const products = await response.json();
    productGrid.replaceChildren();

    if (products.length === 0) {
      productGrid.innerHTML = '<div class="empty">No products found. Try another search.</div>';
    } else {
      products.forEach(product => {
        const card = document.createElement("article");
        card.className = "product-card";
        const image = document.createElement("img");
        image.src = safeImage(product.image_url);
        image.alt = product.name;
        image.loading = "lazy";
        image.onerror = () => { image.src = "https://placehold.co/600x400?text=Product"; };
        const content = document.createElement("div");
        content.className = "card-content";
        const category = document.createElement("span");
        category.className = "category";
        category.textContent = product.category;
        const title = document.createElement("h2");
        title.textContent = product.name;
        const description = document.createElement("p");
        description.textContent = product.description;
        const bottom = document.createElement("div");
        bottom.className = "card-bottom";
        const price = document.createElement("span");
        price.className = "price";
        price.textContent = currency(product.price);
        const button = document.createElement("button");
        button.className = "details-button";
        button.textContent = "View details";
        button.addEventListener("click", () => showDetails(product.id));
        bottom.append(price, button);
        content.append(category, title, description, bottom);
        card.append(image, content);
        productGrid.append(card);
      });
    }
    statusText.textContent = `${products.length} product${products.length === 1 ? "" : "s"} found`;
  } catch (error) {
    statusText.textContent = error.message;
  }
}

async function showDetails(id) {
  try {
    const response = await fetch(`/api/products/${id}`);
    const product = await response.json();
    if (!response.ok) throw new Error(product.error || "Unable to load details.");
    document.getElementById("modalImage").src = safeImage(product.image_url);
    document.getElementById("modalImage").alt = product.name;
    document.getElementById("modalTitle").textContent = product.name;
    document.getElementById("modalCategory").textContent = product.category;
    document.getElementById("modalDescription").textContent = product.description;
    document.getElementById("modalPrice").textContent = currency(product.price);
    modal.classList.remove("hidden");
  } catch (error) {
    statusText.textContent = error.message;
  }
}

document.getElementById("closeModal").addEventListener("click", () => modal.classList.add("hidden"));
modal.addEventListener("click", event => {
  if (event.target === modal) modal.classList.add("hidden");
});
document.addEventListener("keydown", event => {
  if (event.key === "Escape") modal.classList.add("hidden");
});
searchInput.addEventListener("input", loadProducts);
categoryFilter.addEventListener("change", loadProducts);
loadProducts();
