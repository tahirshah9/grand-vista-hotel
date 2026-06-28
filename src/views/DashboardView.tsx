import { useEffect, useState } from 'react';
import { BedDouble, CalendarDays, Receipt, Users } from 'lucide-react';

export default function DashboardView() {
  const [stats, setStats] = useState({ totalRooms: 0, availableRooms: 0, activeBookings: 0, todayRevenue: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/dashboard')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch dashboard');
        return res.json();
      })
      .then(data => {
        if (data.error) throw new Error(data.error);
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  const cards = [
    { title: 'Total Rooms', value: stats.totalRooms, icon: BedDouble, color: 'text-blue-500' },
    { title: 'Available Rooms', value: stats.availableRooms, icon: BedDouble, color: 'text-green-500' },
    { title: 'Active Bookings', value: stats.activeBookings, icon: CalendarDays, color: 'text-orange-500' },
    { title: "Today's Revenue", value: `$${stats.todayRevenue.toFixed(2)}`, icon: Receipt, color: 'text-purple-500' },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="bg-white dark:bg-gray-950 p-6 rounded-xl border border-gray-200 dark:border-gray-800 flex items-center gap-4 shadow-sm">
              <div className={`p-4 rounded-lg bg-gray-50 dark:bg-gray-900 ${card.color}`}>
                <Icon size={24} />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{card.title}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{card.value}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
