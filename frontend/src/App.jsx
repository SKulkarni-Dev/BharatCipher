import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '@/hooks/useAuth';
import { AppLayout } from '@/layouts/AppLayout';
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';
import Investigations from '@/pages/Investigations';
import NewInvestigation from '@/pages/NewInvestigation';
import InvestigationDetails from '@/pages/InvestigationDetails';
import Sources from '@/pages/Sources';
import EntityExplorer from '@/pages/EntityExplorer';
import InvestigationGraph from '@/pages/InvestigationGraph';
import Timeline from '@/pages/Timeline';
import AttributionAssessment from '@/pages/AttributionAssessment';
import ChallengeAttribution from '@/pages/ChallengeAttribution';
import Alerts from '@/pages/Alerts';
import EvidenceExplorer from '@/pages/EvidenceExplorer';
import Settings from '@/pages/Settings';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/investigations" element={<Investigations />} />
            <Route path="/investigations/new" element={<NewInvestigation />} />
            <Route path="/investigations/:caseId" element={<InvestigationDetails />} />
            <Route path="/sources" element={<Sources />} />
            <Route path="/entities" element={<EntityExplorer />} />
            <Route path="/graph" element={<InvestigationGraph />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/attribution" element={<AttributionAssessment />} />
            <Route path="/attribution/challenge" element={<ChallengeAttribution />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/evidence" element={<EvidenceExplorer />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
