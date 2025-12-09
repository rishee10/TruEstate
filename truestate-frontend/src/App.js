import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sales from "./pages/Sales";
import SalesTable from "./components/SalesTable"
// import "./src/App"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Sales />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;


