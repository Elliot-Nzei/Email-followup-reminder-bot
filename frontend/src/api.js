export async function getFollowUps() {
  const response = await fetch("http://localhost:8000/followups", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    }
  });
  return response.json();
}