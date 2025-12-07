<script>
document.getElementById('link-button').onclick = async function() {
  const response = await fetch('/link/token/create', { method: 'POST' });
  const data = await response.json();

  const handler = Plaid.create({
    console.log(data.link_token)
    token: data.link_token,
    onSuccess: async function(public_token, metadata) {
      const res = await fetch('/item/public_token/exchange', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ public_token })
      });

      const json = await res.json();
      console.log('Access token response:', json);
      alert('Bank linked successfully!');
    },
    onExit: function(err, metadata) {
      if (err) console.error('User exited with error:', err);
      else console.log('User exited:', metadata);
    }
  });

  handler.open();
};
</script>

