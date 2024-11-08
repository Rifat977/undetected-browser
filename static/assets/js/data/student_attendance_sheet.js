new gridjs.Grid({
  columns: [
    {
      name: "Student ID",
      width: "80px",
      formatter: function (e) {
        return gridjs.html('<span class="fw-semibold">' + e + "</span>");
      },
    },
    { name: "Name", width: "150px" },
    {
      name: "Status",
      width: "220px",
      formatter: function (e) {
        const statusClass = e === "Present" 
          ? "bg-success-subtle text-success" 
          : "bg-danger-subtle text-danger";
        return gridjs.html(
          '<span class="badge ' + statusClass + ' p-1">' + e + "</span>"
        );
      },
    },
    {
      name: "Actions",
      width: "100px",
      formatter: () => gridjs.html(`
        <button class="btn btn-sm btn-info edit-button">
          <i class="ti ti-pencil"></i>
        </button>
      `)
    }
  ],
  pagination: { limit: 10 },
  sort: true,
  search: true,
  data: [
    ["221-35-936", "Abdullah Al Mamun", "Present", ""],
    ["221-35-937", "Abul Fatah", "Absent", ""],
    ["221-35-938", "Ayesha Siddiqua", "Present", ""],
    ["221-35-939", "Karim Rahman", "Present", ""],
    ["221-35-940", "Sarah Hossain", "Absent", ""],
    ["221-35-941", "Nurul Islam", "Present", ""],
    ["221-35-942", "Tania Akhter", "Absent", ""],
    ["221-35-943", "Mahmud Hasan", "Present", ""],
    ["221-35-944", "Razia Begum", "Present", ""],
    ["221-35-945", "Jahangir Alam", "Absent", ""],
    ["221-35-946", "Salma Khatun", "Present", ""],
    ["221-35-947", "Habib Ullah", "Absent", ""]
],

}).render(document.getElementById("table-gridjs"));
