"use client";
import { useMemo } from "react";
import ReactFlow, {
  type Node,
  type Edge,
  Background,
  BackgroundVariant,
} from "reactflow";
import "reactflow/dist/style.css";
import { customNodeTypes } from "./custom-nodes";

interface SystemDiagramProps {
  nodes: Node[];
  edges: Edge[];
  dark: boolean;
  width: number;
  height: number;
}

export default function SystemDiagram({
  nodes: rawNodes,
  edges: rawEdges,
  dark,
  width,
  height,
}: SystemDiagramProps) {
  /* inject dark flag into every node's data */
  const nodes = useMemo(
    () =>
      rawNodes.map((n) => ({
        ...n,
        data: { ...n.data, dark },
      })),
    [rawNodes, dark]
  );

  /* style edges for current theme */
  const edges = useMemo(
    () =>
      rawEdges.map((e) => ({
        ...e,
        style: {
          ...e.style,
          stroke: dark ? "#525252" : "#a1a1aa",
        },
        labelStyle: {
          ...e.labelStyle,
          fill: dark ? "#a1a1aa" : "#71717a",
        },
      })),
    [rawEdges, dark]
  );

  return (
    <div
      style={{ width: "100%", height }}
      className="rounded-lg overflow-hidden"
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={customNodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        proOptions={{ hideAttribution: true }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        panOnDrag={false}
        zoomOnScroll={false}
        zoomOnPinch={false}
        zoomOnDoubleClick={false}
        preventScrolling={false}
        minZoom={0.3}
        maxZoom={1.5}
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={20}
          size={1}
          color={dark ? "#1f1f1f" : "#e5e7eb"}
        />
      </ReactFlow>
    </div>
  );
}
