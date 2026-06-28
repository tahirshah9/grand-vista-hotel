import { useEffect, useState } from 'react';

export default function BookingsView() {
  const [reservations, setReservations] = useState<any[]>([]);
  const [guests, setGuests] = useState<any[]>([]);
  const [rooms, setRooms] = useState<any[]>([]);
  
  const [form, setForm] = useState({ guest_id: '', room_id: '', check_in: '', check_out: '' });

  const fetchData = () => {
    fetch('/api/reservations').then(res => res.ok ? res.json() : []).then(setReservations).catch(console.error);
    fetch('/api/guests').then(res => res.ok ? res.json() : []).then(setGuests).catch(console.error);
    fetch('/api/rooms').then(res => res.ok ? res.json() : []).then(setRooms).catch(console.error);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreate = async (e: any) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/reservations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (!res.ok) throw new Error('Failed to create reservation');
      const data = await res.json();
      if (data.error) alert(data.error);
      else {
        setForm({ guest_id: '', room_id: '', check_in: '', check_out: '' });
        fetchData();
      }
    } catch (err) {
      console.error(err);
      alert('Network error while booking room.');
    }
  };

  const handleCancel = async (id: string) => {
    try {
      const res = await fetch(`/api/reservations/${id}`, { method: 'DELETE' });
      if (res.ok) fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleGenerateInvoice = async (id: string) => {
    try {
      const res = await fetch(`/api/invoices/${id}`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to generate invoice');
      const data = await res.json();
      if (data.success) {
        alert("Invoice generated! Go to Invoices tab.");
      }
    } catch (err) {
      console.error(err);
      alert('Network error generating invoice.');
    }
  };

  return (
    <div className="space-y-8">
      {/* New Booking Form */}
      <div className="bg-white dark:bg-gray-950 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">New Booking</h3>
        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
          <div>
            <label className="block text-sm font-medium mb-1">Guest</label>
            <select required value={form.guest_id} onChange={e => setForm({...form, guest_id: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5">
              <option value="">Select Guest...</option>
              {guests.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Room</label>
            <select required value={form.room_id} onChange={e => setForm({...form, room_id: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5">
              <option value="">Select Room...</option>
              {rooms.filter(r => r.status === 'available').map(r => <option key={r.id} value={r.id}>Room {r.room_number} ({r.type})</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Check In</label>
            <input required type="date" value={form.check_in} onChange={e => setForm({...form, check_in: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Check Out</label>
            <input required type="date" value={form.check_out} onChange={e => setForm({...form, check_out: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5" />
          </div>
          <button type="submit" className="bg-blue-600 text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700">
            Book Now
          </button>
        </form>
      </div>

      {/* Bookings Table */}
      <div className="bg-white dark:bg-gray-950 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-50 dark:bg-gray-900 text-gray-500 dark:text-gray-400">
            <tr>
              <th className="p-4 font-medium">ID</th>
              <th className="p-4 font-medium">Guest</th>
              <th className="p-4 font-medium">Room</th>
              <th className="p-4 font-medium">Check In</th>
              <th className="p-4 font-medium">Check Out</th>
              <th className="p-4 font-medium">Status</th>
              <th className="p-4 font-medium">Total</th>
              <th className="p-4 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
            {reservations.map(res => (
              <tr key={res.id}>
                <td className="p-4">{res.id.slice(0,8)}...</td>
                <td className="p-4 font-medium">{res.guest_name}</td>
                <td className="p-4">Room {res.room_number}</td>
                <td className="p-4">{res.check_in}</td>
                <td className="p-4">{res.check_out}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${res.status === 'confirmed' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
                    {res.status}
                  </span>
                </td>
                <td className="p-4">${res.total_amount}</td>
                <td className="p-4 text-right space-x-2">
                  <button onClick={() => handleGenerateInvoice(res.id)} className="text-blue-600 hover:underline">Invoice</button>
                  <button onClick={() => handleCancel(res.id)} className="text-red-600 hover:underline">Cancel</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
