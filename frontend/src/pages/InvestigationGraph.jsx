import { useMemo, useState, useCallback } from 'react';
import ReactFlow, { Background, Controls, MiniMap, Handle, Position } from 'reactflow';
import 'reactflow/dist/style.css';
import { X, User, KeyRound, Wallet, Globe, Server, Mail, ShieldHalf, Eye, HelpCircle } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { RawFields } from '@/components/RawFields';
import { useLatestInvestigation } from '@/hooks/useLatestInvestigation';
import { getEntities, getEntityId } from '@/api/entities';
import { getResolvedRelationships } from '@/api/relationships';
import { getEvidence } from '@/api/evidence';
import { pick, show, EMPTY } from '@/utils/format';

const TYPE_ICON = {
  username: User,
  pgp: KeyRound,
  wallet: Wallet,
  domain: Globe,
  infrastructure: Server,
  email: Mail,
  actor: ShieldHalf,
  observation: Eye,
};

const TYPE_COLOR = {
  username: 'var(--color-info)',
  pgp: 'var(--color-accent)',
  wallet: 'var(--color-success)',
  domain: 'var(--color-warning)',
  infrastructure: 'var(--color-normal)',
  email: 'var(--color-contradiction)',
  actor: 'var(--color-risk)',
  observation: 'var(--color-ink-muted)',
};

function EntityNode({ data }) {
  const entityType = pick(data, ['entity_type', 'type']);
  const Icon = TYPE_ICON[entityType] || HelpCircle;
  const color = TYPE_COLOR[entityType] || 'var(--color-ink-muted)';
  return (
    <div className="rounded-lg border bg-[var(--color-panel-raised)] px-3 py-2 shadow-sm" style={{ borderColor: color, minWidth: 150 }}>
      <Handle type="target" position={Position.Top} style={{ opacity: 0 }} />
      <div className="flex items-center gap-2">
        <div className="flex h-6 w-6 items-center justify-center rounded" style={{ backgroundColor: `color-mix(in srgb, ${color} 20%, transparent)`, color }}>
          <Icon size={13} />
        </div>
        <div className="min-w-0">
          <p className="truncate font-mono text-[11.5px] font-medium text-[var(--color-ink)]">{show(pick(data, ['value', 'name', 'label']))}</p>
          <p className="font-mono text-[9px] uppercase tracking-wider text-[var(--color-ink-faint)]">{show(entityType)}</p>
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} style={{ opacity: 0 }} />
    </div>
  );
}

const nodeTypes = { entity: EntityNode };

// Simple deterministic layered layout so the graph reads clearly without a physics library.
function layoutNodes(entities) {
  const layerCounts = {};
  return entities.map((e) => {
    const id = getEntityId(e);
    const layer = Object.keys(layerCounts).length % 4;
    layerCounts[layer] = (layerCounts[layer] || 0) + 1;
    const indexInLayer = layerCounts[layer] - 1;
    return {
      id,
      type: 'entity',
      data: e,
      position: { x: layer * 260 + 20, y: indexInLayer * 110 + 20 },
    };
  });
}

export default function InvestigationGraph() {
  const { investigation, loading, error, empty } = useLatestInvestigation();
  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);

  const entities = useMemo(() => getEntities(investigation), [investigation]);
  const relationships = useMemo(() => getResolvedRelationships(investigation), [investigation]);
  const evidence = useMemo(() => getEvidence(investigation), [investigation]);

  const nodes = useMemo(() => layoutNodes(entities), [entities]);

  const edges = useMemo(
    () =>
      relationships.map((r, i) => ({
        id: pick(r, ['relationship_id', 'id']) || `REL-${i}`,
        source: r.source_entity_id,
        target: r.target_entity_id,
        label: show(pick(r, ['relationship_type', 'type']), (v) => String(v).replaceAll('_', ' ')),
        data: r,
        animated: (r.strength ?? 0) >= 0.8,
        style: {
          stroke: (r.strength ?? 0) >= 0.8 ? 'var(--color-success)' : (r.strength ?? 0) >= 0.55 ? 'var(--color-accent)' : 'var(--color-ink-faint)',
          strokeWidth: 1 + (r.strength ?? 0.3) * 2,
        },
        labelStyle: { fill: 'var(--color-ink-muted)', fontSize: 10, fontFamily: 'IBM Plex Mono' },
        labelBgStyle: { fill: 'var(--color-base)' },
      })),
    [relationships]
  );

  const onNodeClick = useCallback((_, node) => {
    setSelectedEdge(null);
    setSelectedNode(node.data);
  }, []);

  const onEdgeClick = useCallback((_, edge) => {
    setSelectedNode(null);
    setSelectedEdge(edge.data);
  }, []);

  const edgeEvidence = selectedEdge && Array.isArray(selectedEdge.evidence_ids)
    ? evidence.filter((e) => selectedEdge.evidence_ids.includes(pick(e, ['evidence_id', 'id', '_id'])))
    : [];

  if (loading) return <p className="text-[13px] text-[var(--color-ink-muted)]">Loading graph…</p>;
  if (error) return <p className="text-[13px] text-[var(--color-risk)]">{error.message}</p>;
  if (empty) return <p className="text-[13px] text-[var(--color-ink-muted)]">No investigations yet — run one to populate the graph.</p>;

  return (
    <div className="grid h-[calc(100vh-8.5rem)] grid-cols-1 gap-4 lg:grid-cols-4">
      <Card className="relative overflow-hidden lg:col-span-3">
        {nodes.length === 0 ? (
          <div className="flex h-full items-center justify-center text-[13px] text-[var(--color-ink-muted)]">{EMPTY}</div>
        ) : (
          <ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} onNodeClick={onNodeClick} onEdgeClick={onEdgeClick} fitView proOptions={{ hideAttribution: true }}>
            <Background color="#232A38" gap={20} />
            <Controls className="!bg-[var(--color-panel)] !border-[var(--color-border)]" />
            <MiniMap
              pannable
              zoomable
              maskColor="rgba(10,13,19,0.75)"
              style={{ backgroundColor: 'var(--color-panel)' }}
              nodeColor={(n) => TYPE_COLOR[pick(n.data, ['entity_type', 'type'])] || '#5C6478'}
            />
          </ReactFlow>
        )}
        <div className="pointer-events-none absolute left-3 top-3 rounded-md border border-[var(--color-border)] bg-[var(--color-panel)]/90 px-3 py-2 font-mono text-[10px] text-[var(--color-ink-muted)]">
          Investigation {investigation?.investigation_id} · click a node or edge for details
        </div>
      </Card>

      <Card className="overflow-y-auto">
        {!selectedNode && !selectedEdge && (
          <div className="p-5">
            <p className="mb-3 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Legend</p>
            <div className="space-y-1.5">
              {Object.entries(TYPE_COLOR).map(([type, color]) => (
                <div key={type} className="flex items-center gap-2 text-[12px] text-[var(--color-ink-muted)]">
                  <span className="h-2.5 w-2.5 rounded-sm" style={{ backgroundColor: color }} />
                  {type}
                </div>
              ))}
            </div>
            <p className="mt-5 text-[12px] text-[var(--color-ink-muted)]">Select a node or edge in the graph to inspect entity details or relationship evidence.</p>
          </div>
        )}

        {selectedNode && (
          <div>
            <div className="flex items-start justify-between border-b border-[var(--color-border-soft)] px-5 py-4">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{show(getEntityId(selectedNode))}</p>
                <p className="mt-1 font-display text-[15px] font-semibold text-[var(--color-ink)]">{show(pick(selectedNode, ['value', 'name', 'label']))}</p>
              </div>
              <button onClick={() => setSelectedNode(null)} className="text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]"><X size={16} /></button>
            </div>
            <div className="space-y-2.5 px-5 py-4 text-[13px]">
              <RawFields data={selectedNode} exclude={['entity_id', 'id', '_id']} />
            </div>
          </div>
        )}

        {selectedEdge && (
          <div>
            <div className="flex items-start justify-between border-b border-[var(--color-border-soft)] px-5 py-4">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">{show(pick(selectedEdge, ['relationship_id', 'id']))}</p>
                <p className="mt-1 font-display text-[14px] font-semibold text-[var(--color-ink)]">{show(pick(selectedEdge, ['relationship_type', 'type']), (v) => String(v).replaceAll('_', ' '))}</p>
              </div>
              <button onClick={() => setSelectedEdge(null)} className="text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]"><X size={16} /></button>
            </div>
            <div className="space-y-2.5 px-5 py-4 text-[13px]">
              <RawFields data={selectedEdge} exclude={['relationship_id', 'id', 'source_entity_id', 'target_entity_id', 'evidence_ids']} />
              <div>
                <p className="mb-1.5 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">Source Evidence</p>
                {edgeEvidence.length === 0 && <p className="text-[12px] text-[var(--color-ink-muted)]">{EMPTY}</p>}
                <div className="space-y-2">
                  {edgeEvidence.map((e, i) => (
                    <div key={i} className="rounded-md border border-[var(--color-border)] px-3 py-2">
                      <RawFields data={e} />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
