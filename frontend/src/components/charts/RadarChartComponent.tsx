import React, { CSSProperties, useMemo  } from "react";
import {
  Legend,
  PolarAngleAxis as RPolarAngleAxis,
  PolarRadiusAxis as RPolarRadiusAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

// Cast the components to fix TypeScript issue
const PolarAngleAxis = RPolarAngleAxis as any;
const PolarRadiusAxis = RPolarRadiusAxis as any;


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

const pickColor = (
  explicit?: string,
  options?: Record<string, any>,
  styles?: CSSProperties
) =>
  explicit ||
  options?.lineColor ||
  (styles && (styles as any)["--chart-line-color"]) ||
  "#0EA5E9";

export const RadarChartComponent: React.FC<Props> = ({
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

  const showGrid = options?.showGrid ?? true;
  const showTooltip = options?.showTooltip ?? true;
  const showLegend = options?.showLegend ?? true;
  const showRadiusAxis = options?.showRadiusAxis ?? true;
  const legendPosition = options?.legendPosition || "bottom";
  const resolvedColor = resolveColor(color, options, styles);

  // Extract all metric columns (excluding the labelField column)
  // const metricKeys = data && data.length > 0 ? Object.keys(data[0]).filter((key) => key !== labelField) : [];


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

  // Step 1: Get the metric names (keys for the radar chart)
  const metricKeys = Object.keys(data[0]).filter((key) => key !== labelField); // Excluding the label field (e.g., "pid")

  // Step 2: Organize the data for radar chart (models as series and metrics as axes)
  const modelData = useMemo(() => {
    if (!data || data.length === 0) return [];

    return data.map((row) => {
      const model: any = { metric: row[labelField] }; // Use `labelField` as model name (e.g., "pid")
      
      // Add the values for each metric
      metricKeys.forEach((metric) => {
        model[metric] = row[metric]; // Map the metric values
      });

      return model;
    });
  }, [data, labelField, metricKeys]);

  // Step 3: Get all model names (series)
  const modelNames = useMemo(() => {
    if (!data || data.length === 0) return [];
    return data.map((row) => row[labelField]); // Extract the model names (pid)
  }, [data, labelField]);

  if (modelData.length === 0) {
    return (
      <div id={id} style={containerStyle}>
        <h3 style={{ textAlign: "center" }}>No data available</h3>
      </div>
    );
  }

  

  return (
    <div id={id} style={containerStyle}>
      {title && <h3 style={{ textAlign: "center", marginBottom: "10px" }}>{title}</h3>}
      <ResponsiveContainer width="100%" height={360}>
        <RadarChart 
              data={modelData} 
              margin={{ top: 20, right: 80, bottom: 20, left: 80 }}
              // radar={{ metrics: ["A1 Total", "A2 Total", "B1 Total", "B2 Total", "C1 Total", "C2 Total"]}}
              >
          <PolarGrid />
          <PolarAngleAxis dataKey="metric" />
          <PolarRadiusAxis />
          <Tooltip />
          <Legend verticalAlign={legendPosition} />

          {/* Render each model as a separate radar line */}
          {modelNames.map((modelName) => (
            <Radar
              key={modelName}
              name={modelName}
              dataKey={modelName} // This will represent each model's data
              stroke={color || "#8884d8"}
              fill={color || "#8884d8"}
              fillOpacity={0.6}
              isAnimationActive={options?.animate ?? true}
            />
          ))}
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};