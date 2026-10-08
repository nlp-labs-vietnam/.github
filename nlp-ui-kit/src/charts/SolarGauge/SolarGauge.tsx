import React from "react";

export interface SolarGaugeProps {
  /** Current power output in kW */
  currentKw: number;
  /** Installed peak capacity in kWp */
  capacityKwp: number;
  /** Optional label override */
  label?: string;
}

/**
 * SolarGauge — semicircular gauge showing real-time power output as a
 * percentage of installed capacity. Uses only SVG (no third-party chart lib).
 *
 * TODO: Wire up to real-time MQTT / WebSocket feed from the solar inverter API.
 */
export const SolarGauge: React.FC<SolarGaugeProps> = ({
  currentKw,
  capacityKwp,
  label = "Công suất hiện tại",
}) => {
  const pct = Math.min(1, Math.max(0, currentKw / capacityKwp));
  const angle = pct * 180; // 0° → 180° semicircle

  // SVG arc helper
  const polarToCartesian = (cx: number, cy: number, r: number, deg: number) => {
    const rad = ((deg - 90) * Math.PI) / 180;
    return {
      x: cx + r * Math.cos(rad),
      y: cy + r * Math.sin(rad),
    };
  };

  const describeArc = (cx: number, cy: number, r: number, start: number, end: number) => {
    const s = polarToCartesian(cx, cy, r, start);
    const e = polarToCartesian(cx, cy, r, end);
    const large = end - start > 180 ? 1 : 0;
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
  };

  const CX = 100;
  const CY = 100;
  const R  = 80;

  const trackPath  = describeArc(CX, CY, R, -90, 90);       // full 180°
  const valuePath  = describeArc(CX, CY, R, -90, -90 + angle); // filled portion

  return (
    <div className="flex flex-col items-center gap-2">
      <svg viewBox="0 0 200 120" className="w-48" aria-label={label}>
        {/* Track */}
        <path
          d={trackPath}
          fill="none"
          stroke="#e2e8f0"
          strokeWidth="16"
          strokeLinecap="round"
        />
        {/* Value arc */}
        <path
          d={valuePath}
          fill="none"
          stroke="#f59e0b"
          strokeWidth="16"
          strokeLinecap="round"
        />
        {/* Center text */}
        <text
          x={CX}
          y={CY - 4}
          textAnchor="middle"
          className="fill-neutral-900"
          fontSize="22"
          fontWeight="bold"
        >
          {currentKw.toFixed(1)}
        </text>
        <text
          x={CX}
          y={CY + 16}
          textAnchor="middle"
          className="fill-neutral-500"
          fontSize="11"
        >
          kW
        </text>
      </svg>

      <div className="text-center">
        <p className="text-xs font-medium text-neutral-500">{label}</p>
        <p className="text-xs text-neutral-400">
          {(pct * 100).toFixed(0)}% / {capacityKwp} kWp
        </p>
      </div>
    </div>
  );
};
