import { useEffect, useState } from "react";
import api from "../api/api";
import SalesTable from "../components/SalesTable";

function Sales() {
  const [sales, setSales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  // ✅ TEMP FILTER STATE
  const [tempStatus, setTempStatus] = useState("");
  const [tempPayment, setTempPayment] = useState("");
  const [tempRegion, setTempRegion] = useState("");
  const [tempCustomerType, setTempCustomerType] = useState("");
  const [tempCategory, setTempCategory] = useState("");
  const [tempBrand, setTempBrand] = useState("");
  const [tempSearch, setTempSearch] = useState("");

  const [tempGender, setTempGender] = useState("");
  const [tempAgeMin, setTempAgeMin] = useState("");
  const [tempAgeMax, setTempAgeMax] = useState("");
  const [tempStartDate, setTempStartDate] = useState("");
  const [tempEndDate, setTempEndDate] = useState("");
  const [tempTag, setTempTag] = useState("");

  const [filters, setFilters] = useState({});

  useEffect(() => {
    setLoading(true);

    const params = new URLSearchParams({
      page,
      ...filters,
    }).toString();

    api
      .get(`sales/?${params}`)
      .then(res => setSales(res.data.results))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [page, filters]);

  const applyFilters = () => {
    setPage(1);
    setFilters({
      order_status: tempStatus,
      payment_method: tempPayment,
      "customer__region": tempRegion,
      "customer__customer_type": tempCustomerType,
      "product__category": tempCategory,
      "product__brand": tempBrand,
      gender: tempGender,
      age_min: tempAgeMin,
      age_max: tempAgeMax,
      start_date: tempStartDate,
      end_date: tempEndDate,
      tags: tempTag,
      search: tempSearch,
    });
  };

  return (
    <div style={{ padding: 20, backgroundColor: "#f4f6fa", minHeight: "100vh" }}>

      <h1 style={{ marginBottom: 20, color: "#1e3a8a" }}>
        📊 Sales Dashboard
      </h1>

      {/* ✅ STYLED FILTER PANEL */}
      <div
        style={{
          background: "#ffffff",
          padding: 15,
          borderRadius: 10,
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          marginBottom: 20,
        }}
      >
        <h3 style={{ marginBottom: 12 }}>Filters</h3>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: 10,
          }}
        >
          <input placeholder="Search" onChange={e => setTempSearch(e.target.value)} />

          <select onChange={e => setTempGender(e.target.value)}>
            <option value="">All Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>

          <input type="number" placeholder="Min Age" onChange={e => setTempAgeMin(e.target.value)} />
          <input type="number" placeholder="Max Age" onChange={e => setTempAgeMax(e.target.value)} />

          <input type="date" onChange={e => setTempStartDate(e.target.value)} />
          <input type="date" onChange={e => setTempEndDate(e.target.value)} />

          <input placeholder="Tag" onChange={e => setTempTag(e.target.value)} />

          <select onChange={e => setTempStatus(e.target.value)}>
            <option value="">All Status</option>
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
            <option value="Returned">Returned</option>
          </select>

          <select onChange={e => setTempPayment(e.target.value)}>
            <option value="">All Payment</option>
            <option value="UPI">UPI</option>
            <option value="Credit Card">Credit Card</option>
            <option value="Debit Card">Debit Card</option>
          </select>

          <select onChange={e => setTempRegion(e.target.value)}>
            <option value="">Region</option>
            <option value="North">North</option>
            <option value="South">South</option>
            <option value="East">East</option>
            <option value="West">West</option>
          </select>

          <select onChange={e => setTempCustomerType(e.target.value)}>
            <option value="">Customer Type</option>
            <option value="New">New</option>
            <option value="Returning">Returning</option>
            <option value="Loyal">Loyal</option>
          </select>

          <select onChange={e => setTempCategory(e.target.value)}>
            <option value="">Category</option>
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Beauty">Beauty</option>
          </select>

          <select onChange={e => setTempBrand(e.target.value)}>
            <option value="">Brand</option>
            <option value="VoltEdge">VoltEdge</option>
            <option value="StreetLayer">StreetLayer</option>
            <option value="SilkSkin">SilkSkin</option>
          </select>
        </div>

        <button
          onClick={applyFilters}
          style={{
            marginTop: 15,
            padding: "10px 22px",
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: 6,
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          Apply Filters
        </button>
      </div>

      {/* ✅ TABLE */}
      {loading ? <h3>Loading...</h3> : <SalesTable sales={sales} />}

      {/* ✅ PAGINATION */}
      <div style={{ marginTop: 20, textAlign: "center" }}>
        <button
          disabled={page === 1}
          onClick={() => setPage(p => p - 1)}
          style={pagerBtn}
        >
          Prev
        </button>

        <span style={{ margin: "0 15px", fontWeight: "bold" }}>
          Page {page}
        </span>

        <button
          onClick={() => setPage(p => p + 1)}
          style={pagerBtn}
        >
          Next
        </button>
      </div>
    </div>
  );
}

const pagerBtn = {
  padding: "8px 16px",
  backgroundColor: "#e5e7eb",
  border: "none",
  borderRadius: 5,
  cursor: "pointer",
  fontWeight: "bold",
};

export default Sales;
