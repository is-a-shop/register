# is-a.shop Subdomain Service

Welcome to the `is-a.shop` free subdomain service\!

This project allows you to get a **free subdomain** like `your-project.is-a.shop` for your open-source projects, personal sites, portfolios, or anything else you're building. It's a great way to give your online presence a professional and memorable touch.

-----

## How to Get a Subdomain

Follow these steps to request your own subdomain:

1.  **Fork this repository:**

      * Navigate to the main repository page on GitHub: **`https://github.com/is-a-shop/register`**
      * Click the **"Fork"** button at the top right of the page. This creates a copy of the repository under your GitHub account.

2.  **Clone your forked repository:**

      * Go to your forked repository (e.g., `https://github.com/your-username/register`).
      * Click the **"Code"** button and copy the HTTPS or SSH URL.
      * Open your terminal or command prompt and clone the repository:
        ```bash
        git clone https://github.com/your-username/register.git
        cd register
        ```

3.  **Create a new branch:**
    It's good practice to create a new branch for your changes:

    ```bash
    git checkout -b add-your-subdomain-name
    ```

    (Replace `your-subdomain-name` with your actual desired subdomain, e.g., `add-my-awesome-project`)

4.  **Create your subdomain configuration file:**

      * Navigate into the `domains/` directory:
        ```bash
        cd domains/
        ```
      * Create a **new JSON file** named after your desired subdomain.
          * **The filename MUST be your desired subdomain name (e.g., `my-awesome-project.json` for `my-awesome-project.is-a.shop`).**
          * You can use the `example.json` file in this directory as a template.
      * **Edit the new file** with your subdomain details. Here are the required fields:
        ```json
        {
          "subdomain": "your-awesome-project",
          "target": "yourusername.github.io",
          "record_type": "CNAME",
          "description": "A brief description of your project or site.",
          "owner": {
            "github_username": "your-github-username",
            "email": "your-email@example.com"
          }
        }
        ```
          * **`subdomain`**: Your desired subdomain name (e.g., `your-awesome-project`). This should match your filename.
          * **`target`**: The destination your subdomain will point to. This is typically:
              * Your **GitHub Pages** URL (e.g., `yourusername.github.io` or `yourusername.github.io/your-repo-name`)
              * Your **Vercel** deployment URL (e.g., `yourproject.vercel.app`)
              * Your **Netlify** deployment URL (e.g., `yourproject.netlify.app`)
              * An **IP address** for an A record (e.g., `"192.0.2.1"`)
          * **`record_type`**: Can be `"CNAME"` (for domain targets) or `"A"` (for IP address targets). **`CNAME` is the default and most common.**
          * **`description`**: A short description of your project.
          * **`owner`**: Your GitHub username and an optional email.

5.  **Add and commit your new file:**

    ```bash
    git add domains/your-awesome-project.json
    git commit -m "feat: Add your-awesome-project.is-a.shop subdomain"
    ```

    (Replace `your-awesome-project.json` with your actual filename)

6.  **Push your branch to your forked repository:**

    ```bash
    git push origin add-your-subdomain-name
    ```

7.  **Open a Pull Request (PR):**

      * Go to your forked repository on GitHub (in your web browser).
      * GitHub will usually show a banner prompting you to "Compare & pull request" for your newly pushed branch. Click it.
      * **Important:** Ensure the base repository is **`is-a-shop/register`** and the base branch is `main`.
      * Provide a clear title and description for your PR (e.g., "Add `my-awesome-project.is-a.shop`").
      * Click **"Create pull request."**

-----

## What Happens Next?

1.  **Review:** We will review your pull request to ensure the file format is correct and the subdomain request is appropriate. We may ask for changes if needed.
2.  **Automation:** Once your pull request is approved and merged into the `main` branch, our automated system (GitHub Actions) will automatically create the DNS record for your chosen subdomain (e.g., `your-awesome-project.is-a.shop`) in Cloudflare.
3.  **Propagation:** DNS changes can take a few minutes to a few hours to propagate globally.
4.  **Configure Your Hosting:** **This is a crucial step\!** After the DNS record is created on our end, you **must** configure your hosting service (e.g., GitHub Pages, Vercel, Netlify) to recognize and serve content for your new custom domain (e.g., `your-awesome-project.is-a.shop`).
      * **For GitHub Pages:** Go to your repository's **Settings** -\> **Pages**, and under "Custom domain," enter `your-awesome-project.is-a.shop` and save.
      * **For Vercel/Netlify:** Follow their documentation for adding a custom domain to your project.

-----

## Need Help?

  * If your GitHub Actions workflow for your PR fails, check the **"Actions"** tab in the main repository for detailed logs. The error messages there can provide crucial clues.
  * If you're still stuck, open an [issue](https://www.google.com/search?q=https://github.com/is-a-shop/register/issues) in this repository, providing as much detail as possible about your problem and the steps you've taken.

-----

## Important Note about `.shop` Domains

The `.shop` Top-Level Domain (TLD) is primarily associated with e-commerce and online stores. While you can use your `is-a.shop` subdomain for any project, keep this association in mind for your audience.