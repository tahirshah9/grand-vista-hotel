import { useEffect, useState } from 'react';

export default function RoomsView() {
  const [rooms, setRooms] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('All');

  const fetchRooms = () => {
    fetch('/api/rooms')
      .then(res => res.ok ? res.json() : Promise.reject(new Error('Failed to fetch rooms')))
      .then(data => {
        setRooms(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  const changeStatus = (id: string, newStatus: string) => {
    fetch(`/api/rooms/${id}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    }).then(res => res.ok ? fetchRooms() : Promise.reject(new Error('Failed to update status')))
      .catch(console.error);
  };

  if (loading) return <div>Loading rooms...</div>;

  const filtered = filterType === 'All' ? rooms : rooms.filter(r => r.type === filterType);

  return (
    <div className="space-y-6">
      <div className="flex gap-4">
        {['All', 'SingleRoom', 'DoubleRoom', 'DeluxeRoom', 'Suite'].map(type => (
          <button
            key={type}
            onClick={() => setFilterType(type)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filterType === type
                ? 'bg-blue-600 text-white'
                : 'bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800'
            }`}
          >
            {type.replace('Room', ' Room')}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filtered.map(room => (
          <div key={room.id} className="bg-white dark:bg-gray-950 p-6 rounded-xl border border-gray-200 dark:border-gray-800 flex flex-col gap-4 shadow-sm">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">Room {room.room_number}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">{room.type.replace('Room', ' Room')} • Floor {room.floor}</p>
              </div>
              <span className={`w-3 h-3 rounded-full ${
                room.status === 'available' ? 'bg-green-500' : 
                room.status === 'occupied' ? 'bg-red-500' : 'bg-orange-500'
              }`} title={room.status}></span>
            </div>
            
            <div className="mt-auto">
              <p className="text-lg font-semibold text-gray-900 dark:text-white">${room.price_per_night}/night</p>
            </div>
            
            <div className="flex gap-2 mt-2">
              <select
                value={room.status}
                onChange={(e) => changeStatus(room.id, e.target.value)}
                className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-sm rounded-lg p-2"
              >
                <option value="available">Available</option>
                <option value="occupied">Occupied</option>
                <option value="maintenance">Maintenance</option>
              </select>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
