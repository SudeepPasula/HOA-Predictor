import React, { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

function LocationMarker({ onMapClick }) {
  const [position, setPosition] = useState(null);

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setPosition([lat, lng]);
      onMapClick(lat, lng);
    },
  });

  return position === null ? null : (
    <Marker position={position}>
      <Popup>Clicked location</Popup>
    </Marker>
  );
}

function App() {
  const [hoaResult, setHoaResult] = useState(null);

  const handleMapClick = async (lat, lon) => {
    setHoaResult("Loading...");

    try {
      const res = await fetch(
        `http://localhost:8000/predict?lat=${lat}&lon=${lon}`
      );
      const data = await res.json();

      console.log("API Response:", data);

      if (data.error) {
        setHoaResult("❌ No parcel found at that location.");
      } else {
        setHoaResult(`🏘️ HOA Probability: ${data.hoa_probability}%`);
      }
    } catch (err) {
      console.error("API Error:", err);
      setHoaResult("🚨 Error contacting backend.");
    }
  };

  return (
    <div style={{ height: "100vh", width: "100vw", position: "relative" }}>
      <MapContainer
        center={[33.2, -96.9]}
        zoom={12}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap contributors"
        />
        <LocationMarker onMapClick={handleMapClick} />
      </MapContainer>

      {hoaResult && (
        <div
          style={{
            position: "absolute",
            bottom: "20px",
            left: "20px",
            zIndex: 9999,
            backgroundColor: "white",
            color: "#111",
            padding: "12px 18px",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
            fontSize: "16px",
            fontWeight: "500",
            maxWidth: "300px",
          }}
        >
          {hoaResult}
        </div>
      )}
    </div>
  );
}

export default App;
