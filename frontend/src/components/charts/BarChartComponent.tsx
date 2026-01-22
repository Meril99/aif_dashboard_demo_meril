import React, { CSSProperties } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
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
) =>
  explicit ||
  options?.barColor ||
  (styles && (styles as any)["--chart-bar-color"]) ||
  "#7f56d9";

export const BarChartComponent: React.FC<Props> = ({
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

  const orientation = options?.orientation || "vertical";
  const showGrid = options?.showGrid ?? true;
  const showLegend = options?.showLegend ?? true;
  const showTooltip = options?.showTooltip ?? true;
  const legendPosition = options?.legendPosition || "top";
  const resolvedColor = resolveColor(color, options, styles);
  const xAxisLabelAngle = options?.xAxisLabelAngle ?? 0;

  // Extract all metric columns (excluding the labelField column)
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
        <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: xAxisLabelAngle ? 100 : 5}} >
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={options?.gridColor} />}
          <XAxis 
                      // dataKey={labelField}
                      // angle={xAxisLabelAngle}
                      // textAnchor={xAxisLabelAngle ? "end" : "middle"}
                      // height={xAxisLabelAngle ? 100 : undefined}
                      // tick={{ fontSize: 8 }}
                    />
          <YAxis />
          {showTooltip && <Tooltip />}
          {showLegend && <Legend verticalAlign={legendPosition} />}

          {metricKeys.map((metricKey) => (
            <Bar
              key={metricKey}
              dataKey={metricKey}
              name={metricKey}
              fill={colorMap[metricKey] || resolveColor(color, options, styles)}
              isAnimationActive={options?.animate ?? true}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};