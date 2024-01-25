'use client';

import App from '@/components/app';
import FeatureFlags from '@/components/featureFlag/featureFlags';

export default function () {
	return (
		<App>
			<FeatureFlags />
		</App>
	);
}
