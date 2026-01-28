import React, { CSSProperties } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Props {
  id: string;
  title?: string;
  color?: string;
  data: any[];
  labelField: string;
  dataField: string;
  options?: Record<string, any>;
  styles?: CSSProperties;
}

const resolveColor = (
  explicit?: string,
  options?: Record<string, any>,
  styles?: CSSProperties
) => {
  return (
    explicit ||
    options?.lineColor ||
    (styles && (styles as any)["--chart-line-color"]) ||
    "#4a90e2"
  );
};

export const LineChartComponent: React.FC<Props> = ({
  id,
  title,
  color,
  data,
  labelField,
  dataField,
  options,
  styles,
}) => {
  const containerStyle: CSSProperties = {
    width: "100%",
    height: "400px",
    marginBottom: "20px",
    ...styles,
  };

  const strokeWidth = options?.lineWidth ?? 2;
  const resolvedColor = resolveColor(color, options, styles);
  const showGrid = options?.showGrid ?? true;
  const showLegend = options?.showLegend ?? true;
  const showTooltip = options?.showTooltip ?? true;
  const legendPosition = options?.legendPosition || "top";
  const xAxisLabelAngle = options?.xAxisLabelAngle ?? 0;

  // Extract all metric columns (excluding the pid column)
  const metricKeys = data && data.length > 0 ? Object.keys(data[0]).filter((key) => key !== labelField) : [];

  // Parse series configuration for colors
  const colorMap: { [key: string]: string } = {};
  if (options?.series) {
    try {
      const parsedSeries = JSON.parse(options.series);
      parsedSeries.forEach((s: any) => {
        if (s.name && s.color) {
          colorMap[s.name] = s.color;
        }
      });
    } catch (e) {
      console.error('Failed to parse series config:', e);
    }
  }

  return (
    <div id={id} style={containerStyle}>
      {title && <h3 style={{ textAlign: "center", marginBottom: "10px" }}>{title}</h3>}
      <ResponsiveContainer width="100%" height={360}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: xAxisLabelAngle ? 100 : 5 }}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={options?.gridColor} />}
          <XAxis 
            dataKey={labelField}
            angle={xAxisLabelAngle}
            textAnchor={xAxisLabelAngle ? "end" : "middle"}
            height={xAxisLabelAngle ? 100 : undefined}
            tick={{ fontSize: 8 }}
          />
          <YAxis />
          {showTooltip && <Tooltip />}
          {showLegend && <Legend verticalAlign={legendPosition} />}

          {metricKeys.map((metricKey) => (
            <Line
              key={metricKey}
              type={options?.curveType || "monotone"}
              dataKey={metricKey}
              name={metricKey}
              stroke={colorMap[metricKey] || resolveColor(color, options, styles)}
              strokeWidth={strokeWidth}
              dot={options?.dotSize ? { r: options.dotSize } : true}
              isAnimationActive={options?.animate ?? true}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};