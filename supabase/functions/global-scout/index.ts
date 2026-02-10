import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Use Deno.serve for the modern Supabase runtime
Deno.serve(async (req) => {
  // 1. Setup Client
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? ''
  )

  try {
    // 2. Fetch the data from your table
    const { data: trends, error } = await supabase
      .from('trending_topics')
      .select('id, topic_name, short_description, platform_icon, hashtags, created_at')
      .order('created_at', { ascending: false })
      .limit(10)

    if (error) throw error

    // 3. Return the exact structure your UIKit code expects
    return new Response(
      JSON.stringify({
        trendingTopics: trends || [],
        publishReadyPosts: [],
        topicDetails: [],
        selectedPostDetails: []
      }),
      { 
        headers: { "Content-Type": "application/json" },
        status: 200 
      }
    )

  } catch (err) {
    // If it fails, this will show the real error in the curl response
    console.error("Crash Log:", err.message)
    return new Response(JSON.stringify({ error: err.message }), {
      headers: { "Content-Type": "application/json" },
      status: 500
    })
  }
})