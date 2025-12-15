import React, { useEffect, useRef, useState, useCallback } from "react";
import { KGVisualization as KGVisData, KGNode, KGEdge } from "../types";

type Props = {
  data?: KGVisData;
  selectedAgent?: string;
  highlightPath?: string[];
};

type NodePosition = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  fx?: number | null;
  fy?: number | null;
};

type LayoutType = "force" | "hierarchical" | "circular";

export const KGVisualization: React.FC<Props> = ({
  data,
  selectedAgent,
  highlightPath = [],
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [layoutType, setLayoutType] = useState<LayoutType>("force");
  const [isDragging, setIsDragging] = useState(false);
  const [dragNode, setDragNode] = useState<string | null>(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const animationFrameRef = useRef<number | null>(null);
  const nodePositionsRef = useRef<Map<string, NodePosition>>(new Map());
  const simulationRunningRef = useRef(false);
  const nodesRef = useRef<KGNode[]>([]);
  const edgesRef = useRef<KGEdge[]>([]);

  // Force simulation parameters
  const alphaRef = useRef(1);
  const alphaDecay = 0.0228;
  const alphaMin = 0.001;

  const getNodeColor = (type: string): string => {
    const baseColors: Record<string, string> = {
      "Agent": "#FFD700",        // Gold/Yellow for agents
      "SpecializedAgent": "#FFD700",
      "Capability": "#90EE90",   // Light green for capabilities
      "TaskType": "#87CEEB",     // Sky blue for task types
      "Query": "#FFB6C1",        // Light pink for queries
      "RoutingDecision": "#DDA0DD", // Plum for routing decisions
    };
    return baseColors[type] || "#C0C0C0"; // Silver fallback
  };

  const getEdgeColor = (type: string): string => {
    const edgeColors: Record<string, string> = {
      "HAS_CAPABILITY": "rgba(144, 238, 144, 0.6)",
      "REQUIRES_CAPABILITY": "rgba(135, 206, 235, 0.6)",
      "ROUTED_TO": "rgba(221, 160, 221, 0.6)",
      "SOURCE_QUERY": "rgba(255, 182, 193, 0.6)",
      "FALLBACK_AGENT": "rgba(255, 215, 0, 0.6)",
    };
    return edgeColors[type] || "rgba(192, 192, 192, 0.5)";
  };

  // Force simulation
  const tick = useCallback(() => {
    if (!canvasRef.current || !simulationRunningRef.current) return;

    const canvas = canvasRef.current;
    const nodePositions = nodePositionsRef.current;
    const nodes = nodesRef.current;
    const edges = edgesRef.current;

    if (nodes.length === 0) return;

    const width = canvas.width;
    const height = canvas.height;
    const k = Math.sqrt((width * height) / nodes.length);

    // Reset forces
    nodePositions.forEach((pos) => {
      if (pos.fx === null || pos.fx === undefined) {
        pos.vx = 0;
        pos.vy = 0;
      }
    });

    // Repulsion force (all nodes repel each other)
    nodes.forEach((node1) => {
      const pos1 = nodePositions.get(node1.id);
      if (!pos1 || pos1.fx !== null && pos1.fx !== undefined) return;

      nodes.forEach((node2) => {
        if (node1.id === node2.id) return;
        const pos2 = nodePositions.get(node2.id);
        if (!pos2 || pos2.fx !== null && pos2.fx !== undefined) return;

        const dx = pos1.x - pos2.x;
        const dy = pos1.y - pos2.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const force = (k * k) / dist;
        
        pos1.vx += (dx / dist) * force * 0.01;
        pos1.vy += (dy / dist) * force * 0.01;
      });
    });

    // Attraction force (connected nodes attract)
    edges.forEach((edge) => {
      const pos1 = nodePositions.get(edge.source);
      const pos2 = nodePositions.get(edge.target);
      if (!pos1 || !pos2) return;
      if (pos1.fx !== null && pos1.fx !== undefined) return;
      if (pos2.fx !== null && pos2.fx !== undefined) return;

      const dx = pos2.x - pos1.x;
      const dy = pos2.y - pos1.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const force = (dist * dist) / k;
      
      pos1.vx += (dx / dist) * force * 0.01;
      pos1.vy += (dy / dist) * force * 0.01;
      pos2.vx -= (dx / dist) * force * 0.01;
      pos2.vy -= (dy / dist) * force * 0.01;
    });

    // Update positions
    nodePositions.forEach((pos) => {
      if (pos.fx === null || pos.fx === undefined) {
        pos.vx *= 0.6; // Friction
        pos.vy *= 0.6;
        pos.x += pos.vx;
        pos.y += pos.vy;

        // Keep within bounds
        const radius = 20;
        pos.x = Math.max(radius, Math.min(width - radius, pos.x));
        pos.y = Math.max(radius, Math.min(height - radius, pos.y));
      }
    });

    // Decay alpha
    alphaRef.current = Math.max(alphaMin, alphaRef.current - alphaDecay);

    // Render
    render();

    // Continue simulation if alpha is above minimum
    if (alphaRef.current > alphaMin) {
      animationFrameRef.current = requestAnimationFrame(tick);
    } else {
      simulationRunningRef.current = false;
    }
  }, []);

  // Render function
  const render = useCallback(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const nodePositions = nodePositionsRef.current;
    const nodes = nodesRef.current;
    const edges = edgesRef.current;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw edges first (behind nodes)
    if (edges && edges.length > 0) {
      edges.forEach((edge) => {
        const source = nodePositions.get(edge.source);
        const target = nodePositions.get(edge.target);
        if (source && target) {
          const dx = target.x - source.x;
          const dy = target.y - source.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          // Calculate edge midpoint for label
          const midX = (source.x + target.x) / 2;
          const midY = (source.y + target.y) / 2;

          // Draw edge line
          ctx.strokeStyle = getEdgeColor(edge.type);
          ctx.lineWidth = 1.5;
          ctx.globalAlpha = 0.6;
          ctx.beginPath();
          ctx.moveTo(source.x, source.y);
          ctx.lineTo(target.x, target.y);
          ctx.stroke();

          // Draw arrowhead
          const angle = Math.atan2(dy, dx);
          const arrowLength = 6;
          const arrowAngle = Math.PI / 6;
          const arrowX = target.x - 18 * Math.cos(angle);
          const arrowY = target.y - 18 * Math.sin(angle);

          ctx.beginPath();
          ctx.moveTo(arrowX, arrowY);
          ctx.lineTo(
            arrowX - arrowLength * Math.cos(angle - arrowAngle),
            arrowY - arrowLength * Math.sin(angle - arrowAngle)
          );
          ctx.moveTo(arrowX, arrowY);
          ctx.lineTo(
            arrowX - arrowLength * Math.cos(angle + arrowAngle),
            arrowY - arrowLength * Math.sin(angle + arrowAngle)
          );
          ctx.stroke();

          // Draw edge label
          ctx.save();
          ctx.translate(midX, midY);
          ctx.rotate(angle);
          ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
          ctx.font = "10px -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          
          // Label background
          const labelText = edge.type;
          const metrics = ctx.measureText(labelText);
          const labelWidth = metrics.width;
          const labelHeight = 14;
          ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
          ctx.fillRect(-labelWidth / 2 - 3, -labelHeight / 2, labelWidth + 6, labelHeight);
          
          // Label text
          ctx.fillStyle = "#fff";
          ctx.fillText(labelText, 0, 0);
          ctx.restore();

          ctx.globalAlpha = 1.0;
        }
      });
    }

    // Draw nodes
    nodes.forEach((node) => {
      const pos = nodePositions.get(node.id);
      if (!pos) return;

      const isSelected = selectedAgent && node.label === selectedAgent;
      const isHovered = hoveredNode === node.id;
      const isHighlighted = highlightPath.includes(node.id);

      const nodeRadius = isSelected || isHovered ? 22 : 18;

      // Node circle
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, nodeRadius, 0, 2 * Math.PI);
      
      // Node fill
      let fillColor = getNodeColor(node.type);
      if (isSelected) fillColor = "#4CAF50";
      if (isHighlighted) fillColor = "#FFC107";
      
      ctx.fillStyle = fillColor;
      ctx.fill();
      
      // Node border
      ctx.strokeStyle = isSelected || isHovered ? "#fff" : "rgba(255, 255, 255, 0.5)";
      ctx.lineWidth = isSelected || isHovered ? 3 : 2;
      ctx.stroke();

      // Node label
      const label = node.label.length > 18 ? node.label.substring(0, 15) + "..." : node.label;
      ctx.font = `${isHovered ? "bold " : ""}11px -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      
      // Label background
      const metrics = ctx.measureText(label);
      const labelWidth = metrics.width;
      const labelHeight = 16;
      const labelX = pos.x;
      const labelY = pos.y + nodeRadius + 12;
      
      ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
      ctx.fillRect(labelX - labelWidth / 2 - 4, labelY - labelHeight / 2, labelWidth + 8, labelHeight);
      
      // Label text
      ctx.fillStyle = "#fff";
      ctx.fillText(label, labelX, labelY);
    });
  }, [selectedAgent, highlightPath, hoveredNode]);

  // Initialize layout
  useEffect(() => {
    if (!data || !data.nodes || data.nodes.length === 0) {
      setLoading(false);
      if (data && data.nodes && data.nodes.length === 0) {
        setError("Knowledge graph is empty. Please seed it first.");
      } else {
        setError("No graph data available. Please ensure the knowledge graph is seeded.");
      }
      return;
    }

    if (!canvasRef.current || !containerRef.current) return;

    const canvas = canvasRef.current;
    const container = containerRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Set canvas size
    const updateCanvasSize = () => {
      const rect = container.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = Math.max(600, rect.height);
    };
    updateCanvasSize();

    const nodes = data.nodes;
    const edges = data.edges || [];
    nodesRef.current = nodes;
    edgesRef.current = edges;

    // Initialize node positions
    const nodePositions = new Map<string, NodePosition>();
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    nodes.forEach((node, idx) => {
      if (layoutType === "circular") {
        const angle = (idx / nodes.length) * Math.PI * 2;
        const radius = Math.min(canvas.width, canvas.height) * 0.3;
        nodePositions.set(node.id, {
          x: centerX + Math.cos(angle) * radius,
          y: centerY + Math.sin(angle) * radius,
          vx: 0,
          vy: 0,
        });
      } else {
        // Random initial positions for force layout
        nodePositions.set(node.id, {
          x: centerX + (Math.random() - 0.5) * 200,
          y: centerY + (Math.random() - 0.5) * 200,
          vx: 0,
          vy: 0,
        });
      }
    });

    nodePositionsRef.current = nodePositions;
    alphaRef.current = 1;
    simulationRunningRef.current = true;

    // Start simulation
    if (layoutType === "force") {
      tick();
    } else {
      render();
    }

    setLoading(false);

    // Handle window resize
    const handleResize = () => {
      updateCanvasSize();
      if (layoutType === "force") {
        alphaRef.current = 1;
        simulationRunningRef.current = true;
        tick();
      } else {
        render();
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      simulationRunningRef.current = false;
      window.removeEventListener("resize", handleResize);
    };
  }, [data, layoutType, tick, render]);

  // Mouse interactions
  useEffect(() => {
    if (!canvasRef.current || !data || !data.nodes) return;

    const canvas = canvasRef.current;
    const nodePositions = nodePositionsRef.current;
    const nodes = nodesRef.current;

    const getNodeAt = (x: number, y: number): string | null => {
      for (const node of nodes) {
        const pos = nodePositions.get(node.id);
        if (!pos) continue;
        const dx = x - pos.x;
        const dy = y - pos.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist <= 20) return node.id;
      }
      return null;
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      if (isDragging && dragNode) {
        const pos = nodePositions.get(dragNode);
        if (pos) {
          pos.x = x - dragOffset.x;
          pos.y = y - dragOffset.y;
          pos.fx = pos.x;
          pos.fy = pos.y;
          render();
        }
      } else {
        const nodeId = getNodeAt(x, y);
        setHoveredNode(nodeId);
        canvas.style.cursor = nodeId ? "grab" : "default";
      }
    };

    const handleMouseDown = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const nodeId = getNodeAt(x, y);

      if (nodeId) {
        const pos = nodePositions.get(nodeId);
        if (pos) {
          setIsDragging(true);
          setDragNode(nodeId);
          setDragOffset({ x: x - pos.x, y: y - pos.y });
          canvas.style.cursor = "grabbing";
        }
      }
    };

    const handleMouseUp = () => {
      if (isDragging && dragNode) {
        const pos = nodePositions.get(dragNode);
        if (pos) {
          pos.fx = null;
          pos.fy = null;
        }
      }
      setIsDragging(false);
      setDragNode(null);
      canvas.style.cursor = "default";
    };

    const handleMouseLeave = () => {
      setHoveredNode(null);
      if (isDragging && dragNode) {
        const pos = nodePositions.get(dragNode);
        if (pos) {
          pos.fx = null;
          pos.fy = null;
        }
      }
      setIsDragging(false);
      setDragNode(null);
    };

    canvas.addEventListener("mousemove", handleMouseMove);
    canvas.addEventListener("mousedown", handleMouseDown);
    canvas.addEventListener("mouseup", handleMouseUp);
    canvas.addEventListener("mouseleave", handleMouseLeave);

    return () => {
      canvas.removeEventListener("mousemove", handleMouseMove);
      canvas.removeEventListener("mousedown", handleMouseDown);
      canvas.removeEventListener("mouseup", handleMouseUp);
      canvas.removeEventListener("mouseleave", handleMouseLeave);
    };
  }, [data, isDragging, dragNode, dragOffset, render]);

  if (error) {
    return (
      <div className="kg-visualization">
        <h3>Knowledge Graph Visualization</h3>
        <div className="visualization-error">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="kg-visualization">
        <h3>Knowledge Graph Visualization</h3>
        <p className="muted">No graph data available. Please ensure the knowledge graph is seeded.</p>
      </div>
    );
  }

  return (
    <div className="kg-visualization">
      <div className="visualization-header">
        <h3>Knowledge Graph Visualization</h3>
        <div className="layout-selector">
          <label htmlFor="layout-select">Layout: </label>
          <select
            id="layout-select"
            value={layoutType}
            onChange={(e) => setLayoutType(e.target.value as LayoutType)}
            className="layout-dropdown"
          >
            <option value="force">Force-based layout</option>
            <option value="circular">Circular layout</option>
            <option value="hierarchical">Hierarchical layout</option>
          </select>
        </div>
      </div>
      <div className="visualization-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#FFD700" }}></span>
          <span>Agent</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#90EE90" }}></span>
          <span>Capability</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#87CEEB" }}></span>
          <span>TaskType</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#FFB6C1" }}></span>
          <span>Query</span>
        </div>
      </div>
      <div ref={containerRef} className="kg-canvas-container">
        <canvas ref={canvasRef} className="kg-canvas"></canvas>
        {loading && (
          <div className="visualization-loading">
            <p className="muted">Rendering visualization...</p>
          </div>
        )}
        {data && data.nodes && data.nodes.length > 0 && (
          <div className="visualization-info">
            <p className="muted small">
              {data.nodes.length} nodes, {data.edges?.length || 0} relationships
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
