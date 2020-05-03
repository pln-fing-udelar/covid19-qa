import { Router } from "preact-router";

// Code-splitting is automated for routes
import Home from "../routes/home";
import Search from "../routes/search";
import Faq from "../routes/faq";

function App() {
  return (
    <div class="page-background w-full min-h-screen flex rounded-sm justify-center items-start">
      <Router>
        <Home path="/" />
        <Search path="/search/:question" />
        <Faq path="/faq" />
      </Router>
    </div>
  );
}

export default App;
