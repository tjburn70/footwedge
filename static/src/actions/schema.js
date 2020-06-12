import { schema } from 'normalizr';

export const stat = new schema.Entity('stats');
export const round = new schema.Entity('rounds', {
  stats: [stat]
});
