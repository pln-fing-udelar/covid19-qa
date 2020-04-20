import { Router } from "preact-router";

// Code-splitting is automated for routes
import Home from "../routes/home";
import Search from "../routes/search";

function App() {
  return (
    <main id="app" class="px-4 sm:px-8 md:px-16 lg:px-32 max-w-6xl mx-auto">
      <Router>
        <Home path="/" />
        <Search path="/search/:question" />
      </Router>
    </main>
  );
}

export default App;
