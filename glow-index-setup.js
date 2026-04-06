// glow-index-setup.js

import { createClient } from '@supabase/supabase-js';
import { cookies } from 'next/headers';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);

// Function to check product analysis status
export const checkProductAnalysisStatus = async () => {
  const { data, error } = await supabase
    .from('Product')
    .select('id, analyzed');
  if (error) throw new Error(`Error fetching product analysis: ${error.message}`);
  return data;
};