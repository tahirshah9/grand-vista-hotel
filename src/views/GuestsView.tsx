import { useEffect, useState } from 'react';

export default function GuestsView() {
  const [guests, setGuests] = useState<any[]>([]);
  const [form, setForm] = useState({ name: '', email: '', phone: '', id_proof: '' });
  const [search, setSearch] = useState('');

  const fetchGuests = () => {
    fetch('/api/guests')
      .then(res => res.ok ? res.json() : Promise.reject(new Error('Failed to fetch guests')))
      .then(setGuests)
      .catch(console.error);
  };

  useEffect(() => {
    fetchGuests();
  }, []);

  const handleRegister = async (e: any) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/guests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (!res.ok) throw new Error('Failed to register guest');
      const data = await res.json();
      if (data.error) alert(data.error);
      else {
        setForm({ name: '', email: '', phone: '', id_proof: '' });
        fetchGuests();
      }
    } catch (err) {
      console.error(err);
      alert('Network error while registering guest.');
    }
  };

  const filtered = guests.filter(g => 
    g.name.toLowerCase().includes(search.toLowerCase()) || 
    g.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <div className="bg-white dark:bg-gray-950 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Register New Guest</h3>
        <form onSubmit={handleRegister} className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input required type="text" value={form.name} onChange={e => setForm({...form, name: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input required type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Phone</label>
            <input required type="tel" value={form.phone} onChange={e => setForm({...form, phone: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">ID Proof</label>
            <input required type="text" value={form.id_proof} onChange={e => setForm({...form, id_proof: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5" />
          </div>
          <button type="submit" className="bg-blue-600 text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700">
            Register
          </button>
        </form>
      </div>

      <div className="bg-white dark:bg-gray-950 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <input 
            type="text" 
            placeholder="Search by name or email..." 
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full max-w-md bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-2.5"
          />
        </div>
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-50 dark:bg-gray-900 text-gray-500 dark:text-gray-400">
            <tr>
              <th className="p-4 font-medium">Guest ID</th>
              <th className="p-4 font-medium">Name</th>
              <th className="p-4 font-medium">Email</th>
              <th className="p-4 font-medium">Phone</th>
              <th className="p-4 font-medium">ID Proof</th>
              <th className="p-4 font-medium text-right">Loyalty Points</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
            {filtered.map(guest => (
              <tr key={guest.id} className="hover:bg-gray-50 dark:hover:bg-gray-900/50 cursor-pointer">
                <td className="p-4 text-xs font-mono">{guest.id}</td>
                <td className="p-4 font-medium">{guest.name}</td>
                <td className="p-4">{guest.email}</td>
                <td className="p-4">{guest.phone}</td>
                <td className="p-4">{guest.id_proof}</td>
                <td className="p-4 text-right text-blue-500 font-bold">{guest.loyalty_points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
