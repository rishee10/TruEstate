function SalesTable({ sales }) {
  return (
    <div style={{ display: "flex", justifyContent: "center", width: "100%", marginTop: "30px" }}>
      <table
        style={{
          borderCollapse: "collapse",
          width: "90%",
          textAlign: "center",
          border: "2px solid black",
        }}
      >
        <thead>
          <tr>
            <th style={cell}>Txn</th>
            <th style={cell}>Customer</th>
            <th style={cell}>Phone Number</th>
            <th style={cell}>Age</th>
            <th style={cell}>Region</th>
            <th style={cell}>Product</th>
            <th style={cell}>Category</th>
            <th style={cell}>Qty</th>
            <th style={cell}>Final</th>
            <th style={cell}>Status</th>
            <th style={cell}>Payment</th>
          </tr>
        </thead>

        <tbody>
          {sales.map((row, i) => (
            <tr key={i}>
              <td style={cell}>{row.transaction_id}</td>
              <td style={cell}>{row.customer?.name}</td>
              <td style={cell}>{row.customer?.phone_number}</td>
              <td style={cell}>{row.customer?.age}</td>
              <td style={cell}>{row.customer?.region}</td>
              <td style={cell}>{row.product?.name}</td>
              <td style={cell}>{row.product?.category}</td>
              <td style={cell}>{row.quantity}</td>
              <td style={cell}>₹ {row.final_amount}</td>
              <td style={cell}>{row.order_status}</td>
              <td style={cell}>{row.payment_method}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const cell = {
  border: "1px solid black",
  padding: "8px",
  fontSize: "14px",
};

export default SalesTable;
